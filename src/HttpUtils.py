# -*- coding: utf-8 -*-

import http.cookiejar, urllib.request, urllib.parse
import copy
import re
from bs4 import BeautifulSoup
import json

class HttpUtils:

    # FIXME - This installs a system wide url opener.
    def __init__(self):
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)

    def urlToSoup(self, url, params = None):
        content = self.urlContent(url, params)

        contentstr = content.read()
        soup = BeautifulSoup(contentstr)
        print(content.info())
        print(soup)

        return soup

    def jsonToSoup(self, url, params = None):
        content = self.jsonContent(url, params)

        contentstr = content.read()
        soup = BeautifulSoup(contentstr)
        print(content.info())
        print(soup)

        return soup

    def retrieveUrlToFile(self, destinationFileName, url, params = None):
        content = self.urlContent(url, params)

        with open(destinationFileName, "w") as output:
            output.write(content.read())

    def urlContent(self, url, params = None):
        if params:
            encodedParams = urllib.parse.urlencode(params).encode('utf8')
        else:
            encodedParams = None

        print('Requesting:', url)
        content = urllib.request.urlopen(url, encodedParams)

        return content

    def jsonContent(self, url, params = None):
        if params:
            encodedParams = json.dumps(params).encode('utf8')
        else:
            encodedParams = None

        print('Requesting:', url)
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
        req.add_header('X-Requested-With', 'XMLHttpRequest')
        content = urllib.request.urlopen(req, encodedParams)

        return content
