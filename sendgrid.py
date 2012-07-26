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
        }

    def build_params(self, d=None):
        d = d or {}
        params = dict(api_user=self.api_user, api_key=self.api_key)
        params.update(d)
        return params

    def get_newsletter(self, name):
        url = self.url_base + self.api_urls['newsletter']['get']
        request = requests.get(url, params=self.build_params({"name": name}))
        if request.status_code == 200:
            d = json.loads(request.content)
            return d

    def list_newsletter(self, name=None):
        url = self.url_base + self.api_urls['newsletter']['list']
        if name:
            params = self.build_params({"name": name})
        else:
            params = self.build_params()

        request = requests.get(url, params=params)
        if request.status_code == 200:
            return request.content
        else:
            return request.error
