#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import re
import os
from datetime import *
#from BeautifulSoup4 import *
from bs4 import BeautifulSoup

import HttpUtils
from RecupFactures import StatementRetriever


class CesuStatements(StatementRetriever):
    #_initialUrl = "https://www.cesu.urssaf.fr/cesweb/loginempl.jsp"
    _initialUrl = "https://www.cesu.urssaf.fr/cesweb/connectempl.jsp"
    _attestationsEmploiUrl = "https://www.cesu.urssaf.fr/cesweb/attesemploiempl.jsp"
    _siteRoot = "https://www.cesu.urssaf.fr"
    _billUrl = ""

    def login(self, soup):
        params = {'abonLogin': self.userid,
                  'abonPasswd': self.password}
        soupLogin = self.httpUtils.urlToSoup(self._initialUrl, params)

        soupAttestations = self.httpUtils.urlToSoup(self._attestationsEmploiUrl, None)

        return soupAttestations

    def retrieveMissingStatements(self, soup):
        print("Retrieving missing statements")

        pdfLinks = soup.find_all(href=lambda(value): value and re.match('/cesweb/attesemploi.pdf\?ref=', value))
        for pdfLink in pdfLinks:
            fullLink = self._siteRoot + pdfLink['href']
            print(fullLink)
            #fileName =

        #contentstr = content.read()
        #divs = SoupStrainer('div')
        #soup = MinimalSoup(contentstr, parseOnlyThese=divs)

        #print(contentstr)

        #f = open('/tmp/debug', 'w')
        #f.write(contentstr)

        #Mon Jul 26 00:00:00 CEST 2010
        # match = re.match('.*<div class="malegende">.*date de ma facture : <span class="datelegende">(\w\w\w \w\w\w \d\d \d\d:\d\d:\d\d \w+ \d\d\d\d)</span>', contentstr, re.MULTILINE | re.DOTALL | re.IGNORECASE)

        # if not match:
        #     match = re.match('.*<div class="malegende">.*date de ma facture : <span class="datelegende">(\d\d/\d\d/\d\d)</span>', contentstr, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        #     print(match.group(1))
        #     fileDate = match.group(1)
        #     fileDateIso = datetime.strptime(fileDate, "%d/%m/%y").strftime("%Y-%m-%d");
        # else:
        #     print(match.group(1))
        #     fileDate = match.group(1)
        #     fileDateIso = datetime.strptime(fileDate, "%a %b %d %H:%M:%S %Z %Y").strftime("%Y-%m-%d");

        # print(fileDateIso)

        # destFileName = self.statementsPath + "/Attestation_Emploi-" + fileDateIso + ".pdf"

        # if not os.access(destFileName, os.F_OK):

        #     print("Getting", destFileName)

        #     # Save PDF
        #     if debug:
        #         print("Debug mode -> not downloading")
        #     else:
        #         self.httpUtils.retrieveUrlToFile(destFileName, self._billUrl)

        # else:
        #     print("Already have", destFileName)


statements = CesuStatements(os.environ["HOME"] + "/Documents/Archives/CESU-URSAF/Attestations_Emploi", ##USER, ##PASS)

debug = False

# if debug:
#     f = open('data/ft_page_facture.htm')
#     franceTelecomStatements.retrieveLastStatement(f)
# else:
#     soup = franceTelecomStatements.createSession()
#     content = franceTelecomStatements.login(soup)
#     franceTelecomStatements.retrieveLastStatement(content)


soup1 = statements.createSession()
soup2 = statements.login(soup1)
#print(soup2)
statements.retrieveMissingStatements(soup2)
