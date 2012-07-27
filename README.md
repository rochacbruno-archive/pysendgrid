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
# pass in your credentials

from pysendgrid import SendGrid
sendgrid = SendGrid("you@domain.com", "yourpassword")

# create a new newsletter
# name, subject, html

sendgrid.add_newsletter("teste2", "testando apenas", "<html> bla bla bla </html>")

{u'message': u'success'}

# clone an existing newsletter
# existing_name, new_name

sendgrid.clone_newsletter("teste2", "teste3") 

{u'message': u'success'}

# get a newsletter
# newsletter_name

sendgrid.get_newsletter("teste3")

{u'can_edit': True, u'name': u'teste3', u'text': u'<html> bla bla bla </html>',
u'newsletter_id': 522082, u'total_recipients': 0, u'html': u'<html> bla bla bla </html>', u'type': u'html', u'date_schedule': 0,
u'identity': u'mydomain.com', u'subject': u'testing'}

# list all newsletters

sendgrid.list_newsletter()

[{u'can_edit': True, u'name': u'teste3', u'text': u'<html> bla bla bla </html>', 
u'newsletter_id': 522082, u'total_recipients': 0, u'html': u'<html> bla bla bla </html>', u'type': u'html', u'date_schedule': 0,
u'identity': u'mydomain.com', u'subject': u'testing'},
{u'can_edit': True, u'name': u'teste2', u'text': u'<html> bla bla bla </html>', 
u'newsletter_id': 522081, u'total_recipients': 0, u'html': u'<html> bla bla bla </html>', u'type': u'html', u'date_schedule': 0,
u'identity': u'mydomain.com', u'subject': u'testing'},
..., ...]

# Create a recipient list
# list_name

sendgrid.add_list("potential_customers")

{u'message': u'success'}

# Add emails (one by one) in to a recipient list
# lista_name, recipent_data (must be a dict with name, email and aditional keys)

person = {"name": "John", "email": "jon@jon.com"}
sendgrid.add_email_to("potential_customers", **person)

{u'inserted': 1}

# add multiple emails in to a recipient list
# list_name, list of recipients (a list of dicts)
people = [{"name": "John", "email": "jon@jon.com"}, {"name": "Mary", "email": "mary@mary.com"}]

sendgrid.add_emails_to("potential_customers", people)

{u'inserted': 2}


# Add a recipient list in to a newsletter
# newsletter_name, list_name

sendgrid.add_recipients("teste3", "potential_customers")

{u'message': u'success'}


# Schedule a newsletter to be sent after 30 minutes
# newsletter_name, delay in minutes

sendgrid.add_schedule("teste3", after=30)

{u'message': u'success'}

# schedule a newsletter to be sent in a specific date
# newsletter_name, a datetime object

import datetime
send_date = datetime.datetime(2012, 01, 01)
sendgrid.add_schedule("teste3", at=send_date)

{u'message': u'success'}

# send a newsletter immediatelly
# newsletter_name, ommiting date or delay will send immediatelly

sendgrid.add_schedule("teste3")

{u'message': u'success'}

# send a cloned newsletter to a list (.csv) of recipients
# day by day, starting with 200 and increasing 200 each day
# very useful for ISP warming

# it will take a csv, with no header and in format name,email@domain.com
# will split the csv in to lists starting by 200 and increasing by 200
# exemple:
# my_awesome_list_1: 200 recipients
# my_awesome_list_2: 400 recipients
# my_awesome_list_3: 600 recipients

sendgrid.import_define_send("/path/to/csv_file.csv",
                           "newsletter_to_be_cloned",
                           "My_awesome_name_prefix",
                           interval=200,
                           interval_step=200,
                           start_send_at=datetime.datetime(2012, 7, 29, 18, 9, 0, 798133)
	                       )
 
# will print statuses and stores text file logs
# TODO: use sqlite and DAL for status?
```

# TODO

* calculate date to send (sendgrid does not support timezone)
* implement delete methods
* better docs
* better exception handling
* Map all Newsletter API methods
* pack and distribute, send to PyPi
* Tests
* Import from excel file
