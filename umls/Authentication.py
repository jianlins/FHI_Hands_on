#!/usr/bin/python
## 6/16/2017 - remove PyQuery dependency
## 5/19/2016 - update to allow for authentication based on api-key, rather than username/pw
## See https://documentation.uts.nlm.nih.gov/rest/authentication.html for full explanation

import requests
# from pyquery import PyQuery as pq
import lxml.html as lh
from lxml.html import fromstring

import os

uri = "https://utslogin.nlm.nih.gov"
# option 1 - username/pw authentication at /cas/v1/tickets
# auth_endpoint = "/cas/v1/tickets/"
# option 2 - api key authentication at /cas/v1/api-key
auth_endpoint = "/cas/v1/api-key"


class Authentication:

    # def __init__(self, username,password):
    def __init__(self, apikey=None):
        # self.username=username
        # self.password=password
        if apikey is not None:
            self.apikey = apikey
        elif os.path.isfile('umls/api.key'):
            file = open('umls/api.key', 'r')
            self.apikey = file.read().strip()
            file.close()
        if self.apikey is None or len(self.apikey.strip())==0:
            self.apikey = input("Fill your UMLS api key: ")
            save = input("Do you want to save this api key? (y/n)")
            if save is not None and save.lower().startswith('y'):
                file = open('umls/api.key', 'w')
                file.write(self.apikey)
                file.close()
            pass
        self.service = "http://umlsks.nlm.nih.gov"

    def gettgt(self):
        # params = {'username': self.username,'password': self.password}
        params = {'apikey': self.apikey}
        h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
        r = requests.post(uri + auth_endpoint, data=params, headers=h)
        response = fromstring(r.text)
        ## extract the entire URL needed from the HTML form (action attribute) returned - looks similar to https://utslogin.nlm.nih.gov/cas/v1/tickets/TGT-36471-aYqNLN2rFIJPXKzxwdTNC5ZT7z3B3cTAKfSc5ndHQcUxeaDOLN-cas
        ## we make a POST call to this URL in the getst method
        tgt = response.xpath('//form/@action')[0]
        return tgt

    def getst(self, tgt):
        params = {'service': self.service}
        h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
        r = requests.post(tgt, data=params, headers=h)
        st = r.text
        return st
