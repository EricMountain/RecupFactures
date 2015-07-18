#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os
from datetime import *

import HttpUtils
from RecupFactures import StatementRetriever


class AmeliStatements(StatementRetriever):
    _siteRoot = "https://assure.ameli.fr:443/"
    _initialUrl = _siteRoot

    def login(self, soup):
        print("Logging in")

        form = soup.findAll(action=lambda(value): value and re.match('.*jsessionid.*', value))
        # Barfing here indicates that the web site is probably unavailable (e.g.
        #         L'accès à votre compte ameli est momentanément indisponible.
        #         Une opération de maintenance est en cours.
        #         Veuillez nous excuser pour la gène occasionnée
        actionUrl = form[0]['action']
        params = {'connexioncompte_2numSecuriteSociale': self.userid,
                  'connexioncompte_2codeConfidentiel': self.password,
                  'connexioncompte_2actionEvt': 'connecter'}

        soup = self.httpUtils.urlToSoup(actionUrl, params)

        return soup

    def gotoStatementsPage(self, soup):
        print("Switching to statements' page")

        linkToPrestations = soup.findAll(href=lambda(value): value and re.match('.*as_revele_mensuel_presta_page.*', value))
        linkToPrestationsUrl = linkToPrestations[0]['href']

        soup = self.httpUtils.urlToSoup(linkToPrestationsUrl)

        return soup

    def retrieveStatements(self, soup):
        print("Retrieving statements")

        formsForPdf = soup.findAll(action=lambda(value): value and re.match('.*PDFServlet.dopdf.*', value))

        for formForPdf in formsForPdf:
            formForPdfUrl = self._siteRoot + formForPdf['action']

            input = formForPdf.findAll('input')

            fileDate = input[0]['value']
            fileDateIso = datetime.strptime(fileDate, "%m%d%y").strftime("%Y-%m-%d");
            destFileName = self.statementsPath + "/AssuranceMaladie-ReleveMensuel-" + fileDateIso + ".pdf"

            if not os.access(destFileName, os.F_OK):

                print("Getting", destFileName)

                params = {'PDF.moisRecherche': input[0]['value'],
                          'PDF.type': input[1]['value'],
                          'PDR.titre': input[2]['value']}

                # Save PDF
                self.httpUtils.retrieveUrlToFile(destFileName, formForPdfUrl, params)

            else:
                print("Already have", destFileName)


ameliStatements = AmeliStatements(os.environ["HOME"] + "/Documents/communication/Assurance Maladie", ##USER, ##PASS)
soup = ameliStatements.createSession()
soup = ameliStatements.login(soup)
soup = ameliStatements.gotoStatementsPage(soup)
ameliStatements.retrieveStatements(soup)
