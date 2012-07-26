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
from pysendgrid import SendGrid
sendgrid = SendGrid("you@domain.com", "yourpassword")
existing = sendgrid.get_newsletter("my_newsletter_name")
new = sendgrid.add_newsletter("My new newsletter", subject="awesome news", body="<html>...</html>")
cloned = sendgrid.clone_newsletter("existing_name", "new_name")
```



