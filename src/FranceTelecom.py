#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os
from datetime import *

import HttpUtils
from RecupFactures import StatementRetriever

# BeautifulSoup is not used here because it simply can't cope with FT's HTML.
# And that's saying something…

class FranceTelecomStatements(StatementRetriever):
    _initialUrl = "http://id.orange.fr/"
    _siteRoot = "https://www.espaceclient.francetelecom.com"
    _billUrl = "https://www.espaceclient.francetelecom.com/ecare/servlets/pr_VueFactureEnLigneVisualisationServlet?action=facture"

    def login(self, soup):
        print("Logging in")
        print(soup.prettify())

        #form = soup.findAll(action=lambda(value): value and re.match('form1', value))
        form = soup.findAll("form")
        #print(form)
        #actionUrl = form[0]['action']
        actionUrl = self._initialUrl
        print(actionUrl)
        params = {'user_credential': self.userid,
                  'user_password': self.password}

        soup = self.httpUtils.urlToSoup(actionUrl, params)
        return soup

        #content = self.httpUtils.urlContent(actionUrl, params)
        #return content

    def retrieveLastStatement(self, content):
        print("Retrieving last statement")

        contentstr = content.read()
        #divs = SoupStrainer('div')
        #soup = MinimalSoup(contentstr, parseOnlyThese=divs)

        #print(contentstr)

        f = open('/tmp/debug', 'w')
        f.write(contentstr)

        match = re.match('.*<div class="malegende">.*date de ma facture : <span class="datelegende">(\w\w\w \w\w\w \d\d \d\d:\d\d:\d\d \w+ \d\d\d\d)</span>', contentstr, re.MULTILINE | re.DOTALL | re.IGNORECASE)

        if not match:
            match = re.match('.*<div class="malegende">.*date de ma facture : <span class="datelegende">(\d\d/\d\d/\d\d)</span>', contentstr, re.MULTILINE | re.DOTALL | re.IGNORECASE)
            print(match.group(1))
            fileDate = match.group(1)
            fileDateIso = datetime.strptime(fileDate, "%d/%m/%y").strftime("%Y-%m-%d");
        else:
            print(match.group(1))
            fileDate = match.group(1)
            fileDateIso = datetime.strptime(fileDate, "%a %b %d %H:%M:%S %Z %Y").strftime("%Y-%m-%d");

        print(fileDateIso)

        destFileName = self.statementsPath + "/FranceTelecom-Facture-" + fileDateIso + ".pdf"

        if not os.access(destFileName, os.F_OK):

            print("Getting", destFileName)

            # Save PDF
            if debug:
                print("Debug mode -> not downloading")
            else:
                self.httpUtils.retrieveUrlToFile(destFileName, self._billUrl)

        else:
            print("Already have", destFileName)


franceTelecomStatements = FranceTelecomStatements(os.environ["HOME"] + "/Documents/communication/bills/France Telecom", ##USER, ##PASS)

debug = False

# if debug:
#     f = open('data/ft_page_facture.htm')
#     franceTelecomStatements.retrieveLastStatement(f)
# else:
#     soup = franceTelecomStatements.createSession()
#     content = franceTelecomStatements.login(soup)
#     franceTelecomStatements.retrieveLastStatement(content)

soup = franceTelecomStatements.createSession()
content = franceTelecomStatements.login(soup)
print(soup)
