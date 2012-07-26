# coding: utf-8

import requests
import json


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

    def call(self, api, resource, params=None):
        url = self.build_url(api, resource)
        call_params = self.build_params(params or {})
        request = requests.get(url, params=call_params)
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            return request

    def get_newsletter(self, name):
        return self.call('newsletter', 'get', {"name": name})

    def list_newsletter(self, name=None):
        return self.call('newsletter', 'list', {"name": name} if name else {})

    def add_newsletter(self, name, subject, html, text=None, identity=None):
        if not identity:
            try:
                identity = self.list_identity()[0]['identity']
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
        pass

    def get_email(self, list_name, **fields):
        return self.call('email', 'get', dict(list=list_name, **fields))

    def add_recipients(self, newsletter_name, list_name):
        return self.call('recipients', 'add', {"name": newsletter_name, "list": list_name})

    def add_schedule(self, newsletter_name, at=None, after=None):
        if at:
            d = dict(name=newsletter_name, at=at.isoformat())
        elif after:
            d = dict(name=newsletter_name, after=after)
        else:
            d = dict(name=newsletter_name)
        return self.call('schedule', 'add', d)
