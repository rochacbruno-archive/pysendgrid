# coding: utf-8

from retry import retry_on_exceptions
import requests
import datetime
import time
import json
import csv


class SendGrid(object):
    def __init__(self, api_user, api_key, url_base="https://sendgrid.com"):
        self.api_user = api_user
        self.api_key = api_key
        self.url_base = url_base

        self.api_urls = {
            "newsletter": {  # create, clone, edit newsletter
                "add": "/api/newsletter/add.json",
                "edit": "/api/newsletter/edit.json",
                "list": "/api/newsletter/list.json",
                "get": "/api/newsletter/get.json"},
            "lists": {  # recipient lists
                "add": "/api/newsletter/lists/add.json",
                "edit": "/api/newsletter/lists/edit.json",
                "get": "/api/newsletter/lists/get.json"},
            "email": {  # emails of recipient list
                "add": "/api/newsletter/lists/email/add.json",
                "edit": "/api/newsletter/lists/email/edit.json",
                "get": "/api/newsletter/lists/email/get.json"},
            "recipients": {  # recipients for a newsletter
                "add": "/api/newsletter/recipients/add.json",
                "get": "/api/newsletter/recipients/get.json"},
            "schedule": {  # schedule to send
                "add": "/api/newsletter/schedule/add.json",
                "get": "/api/newsletter/schedule/get.json"},
            "identity": {  # identities for newsletter
                "add": "/api/newsletter/identity/add.json",
                "list": "/api/newsletter/identity/list.json",
                "get": "/api/newsletter/identity/get.json"},
        }

    def build_params(self, d=None):
        d = d or {}
        params = dict(api_user=self.api_user, api_key=self.api_key)
        params.update(d)
        return params

    def build_url(self, api, resource):
        try:
            return self.url_base + self.api_urls[api][resource]
        except KeyError:
            raise("url not found for %s api and %s resource" % (api, resource))

    @retry_on_exceptions(types=[Exception], tries=5, sleep=30)
    def call(self, api, resource, params=None):
        url = self.build_url(api, resource)
        call_params = self.build_params(params or {})
        response = requests.post(url, params=call_params)

        if response.status_code == 200:
            parser = json.loads
        else:
            parser = lambda x: x

        return dict(success=True,
                    status_code=response.status_code,
                    url=response.url,
                    response=parser(response.content))

    def get_newsletter(self, name):
        return self.call('newsletter', 'get', {"name": name})

    def list_newsletter(self, name=None):
        return self.call('newsletter', 'list', {"name": name} if name else {})

    def add_newsletter(self, name, subject, html, text=None, identity=None):
        if not identity:
            try:
                identity = self.list_identity()['response'][0]['identity']
            except Exception:
                raise("You have to inform the identity name")
        text = text or html  # TODO: clean HTML tags
        d = dict(identity=identity,
                 name=name,
                 subject=subject,
                 text=text,
                 html=html)
        return self.call('newsletter', 'add', d)

    def clone_newsletter(self, existing_name, new_name):
        existing = self.get_newsletter(existing_name)
        if isinstance(existing, dict):
            new = self.add_newsletter(
                name=new_name,
                subject=existing['subject'],
                html=existing['html'],
                text=existing['text'],
                identity=existing['identity']
                )
            return new
        return existing

    def list_identity(self, name=None):
        return self.call('identity', 'list', {"name": name} if name else {})

    def add_list(self, name):
        return self.call('lists', 'add', {"list": name})

    def get_list(self, name):
        return self.call('lists', 'get', {"list": name} if name else {})

    def add_email_to(self, list_name, **fields):
        data = json.dumps(fields)
        return self.call('email', 'add', dict(list=list_name, data=data))

    def add_emails_to(self, list_name, emails):
        """adds a list of emails
        [{'email': 'jon@jon.com', 'name': 'Jon'}, {'email': 'mary@mary.com', 'name': 'Mary'}]
        """
        #email_data = []
        for i, email in enumerate(emails):
            emails[i] = json.dumps(email)
        #data = json.dumps(email_data)
        return self.call('email', 'add', dict(list=list_name, data=emails))

    def get_email(self, list_name, **fields):
        return self.call('email', 'get', dict(list=list_name, **fields))

    def add_recipients(self, newsletter_name, list_name):
        times = 10
        while times:
            print "trying to add recipient: %s" % times
            api_call = self.call('recipients', 'add', {"name": newsletter_name, "list": list_name})
            if 'error' in api_call['response']:
                if 'without recipients' in api_call['response']['error']:
                    times -= 1
                    time.sleep(30)
            else:
                times = 0
        return api_call

    def add_schedule(self, newsletter_name, at=None, after=None):
        if at:
            d = dict(name=newsletter_name, at=at.isoformat())
        elif after:
            d = dict(name=newsletter_name, after=after)
        else:
            d = dict(name=newsletter_name)
        return self.call('schedule', 'add', d)

    def import_define_send(self,
                           csv_path,  # name, email csv string (no header)
                           newsletter_name,  # existing newsletter_name to be cloned
                           list_prefix,  # prefix to be used to name newsletter and lists created
                           interval=0,  # the first sending will be for how many recipients?
                           interval_step=0,  # increase interval at step
                           start_count=0,
                           start_send_at=None,  # when to start the sending - datetime object?
                           send_interval=1,  # interval in days
                           keys=("name", "email")
                           ):
        # split csv recipients in groups, by defined interval and increasing
        lists = {}
        lists_send_date = {}
        f = open(csv_path, 'r')
        reader = csv.reader(f)
        out = [dict(zip(keys, prop)) for prop in reader]
        total = len(out)
        send_interval = datetime.timedelta(days=send_interval)
        if start_send_at:
            day_start = start_send_at
        else:
            day_start = datetime.datetime.now() + send_interval
        assert isinstance(day_start, datetime.datetime), "start_send_at must be datetime"
        if not interval:
            interval = 500
        if not interval_step:
            interval_step = 200
        for i in xrange(total):
            if start_count < interval:
                l = lists.setdefault(str(day_start.isoformat()), [])
                lists_send_date.setdefault(str(day_start.isoformat()), day_start)
                l.append(out[i])
                start_count += 1
            else:
                day_start += send_interval
                interval += interval_step
                start_count = 0
                l = lists.setdefault(str(day_start.isoformat()), [])
                lists_send_date.setdefault(str(day_start.isoformat()), day_start)
                l.append(out[i])

        # create a list for each group of recipients
        list_names = lists.keys()
        for list_name in list_names:
            print "Creating list %s" % list_name
            print self.add_list(list_prefix + "_" + list_name), list_name

        # clone the newsletter for each froup of recipients
        for list_name in list_names:
            print "Cloning newsletter %s in to %s" % (newsletter_name, list_prefix + "_" + list_name)
            print self.clone_newsletter(newsletter_name, list_prefix + "_" + list_name)

        # add recipients to each created list
        already_included = []
        # reads the status file
        try:
            with open(list_prefix + "_status.txt", 'r') as status:
                for line in status:
                    d = json.loads(line)
                    already_included.append(d['email'])
        except:
            pass  # first time, no need to read

        # call the api for each recipient
        for list_name, recipients in lists.items():
            for i, recipient in enumerate(recipients):
                if not recipient['email'] in already_included:
                    try:
                        print list_name, i, recipient['email'], self.add_email_to(list_prefix + "_" + list_name, **recipient)
                        with open(list_prefix + "_status.txt", 'a') as status:
                            msg = json.dumps(recipient) + "\n"
                            status.write(msg)
                    except Exception, e:
                        with open(list_prefix + "_error.txt", 'a') as error:
                            print str(e)
                            error.write(str(e) + str(datetime.datetime.now()))

        # add each list to respective newsletter
        for list_name in list_names:
            print "adding list %s to newsletter %s" % (list_name, list_prefix + "_" + list_name)
            print self.add_recipients(list_prefix + "_" + list_name, list_prefix + "_" + list_name)

        # scheduling the sending for the respective date
        for list_name in list_names:
            print "Schedulling sending for %s" % list_prefix + "_" + list_name
            date_to_send = lists_send_date[list_name]
            print self.add_schedule(list_prefix + "_" + list_name, at=date_to_send)
