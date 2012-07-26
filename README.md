pysendgrid
==========

Python module for interacting with sendgrid api

Requirements
------------

* json
* requests

Features
--------

* Newsletter API

How to use
----------

```python

# Create sendgrid object

from pysendgrid import SendGrid
sendgrid = SendGrid("you@domain.com", "yourpassword")

# create a new newsletter

sendgrid.add_newsletter("teste2", "testando apenas", "<html> bla bla bla </html>")

{u'message': u'success'}

# clone an existing newsletter

sendgrid.clone_newsletter("teste2", "teste3") 

{u'message': u'success'}

# get a newsletter

sendgrid.get_newsletter("teste3")

{u'can_edit': True, u'name': u'teste3', u'text': u'<html> bla bla bla </html>', u'newsletter_id': 522082, u'total_recipients': 0, u'html': u'<html> bla bla bla </html>', u'type': u'html', u'date_schedule': 0, u'identity': u'mydomain.com', u'subject': u'testing'}

# list all newsletters

sendgrid.list_newsletter()

[{u'can_edit': True, u'name': u'teste3', u'text': u'<html> bla bla bla </html>', u'newsletter_id': 522082, u'total_recipients': 0, u'html': u'<html> bla bla bla </html>', u'type': u'html', u'date_schedule': 0, u'identity': u'mydomain.com', u'subject': u'testing'}, {u'can_edit': True, u'name': u'teste2', u'text': u'<html> bla bla bla </html>', u'newsletter_id': 522081, u'total_recipients': 0, u'html': u'<html> bla bla bla </html>', u'type': u'html', u'date_schedule': 0, u'identity': u'mydomain.com', u'subject': u'testing'} ..., ...]

# Create a recipient list

sendgrid.add_list("potential_customers")

{u'message': u'success'}

# Add emails (one by one) in to a recipient list

people = [{"name": "John", "email": "jon@jon.com"}, {"name": "Mary", "email": "mary@mary.com"}, ...]

for person in people:
    sendgrid.add_email_to("potential_customers", **person)

{u'message': u'success'}
{u'message': u'success'}
...

# Add a recipient list in to a newsletter

sendgrid.add_recipients("teste3", "potential_customers")

{u'message': u'success'}


# Schedule a newsletter to be sent after 30 minutes

sendgrid.add_schedule("teste3", after=30)

{u'message': u'success'}

# schedule a newsletter to be sent in a specific date

import datetime
send_date = datetime.datetime(2012, 01, 01)
sendgrid.add_schedule("teste3", at=send_date)

{u'message': u'success'}

# send a newsletter immediatelly

sendgrid.add_schedule("teste3")

{u'message': u'success'}

```

# TODO

* add multiple recipients in one request (bulk add)
* calculate date to send (sendgrid does not support timezone)



