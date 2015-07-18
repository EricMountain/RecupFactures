#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os
from datetime import *
from bs4 import BeautifulSoup

import HttpUtils
from RecupFactures import StatementRetriever



class ScolInfo(StatementRetriever):
    _siteRoot = "http://www.scolinfo.net/"
    _initialUrl = _siteRoot + "Default.aspx"

    def login(self, soup):
        print("Logging in")
        actionUrl = self._initialUrl
        params = {"LoginControl$UserName": self.userid,
                  "LoginControl$Password": self.password,
                  "__LASTFOCUS": "",
                  "__EVENTTARGET": "LoginControl$LoginButton",
                  "__EVENTARGUMENT": ""}
        soup = self.httpUtils.urlToSoup(actionUrl, params)

        form = soup.find(id="form1")
        action = form['action']
        viewstate_name = form.input['name']
        viewstate_value = form.input['value']
        print(action, viewstate_name, viewstate_value)

        params = {viewstate_name: viewstate_value,
                  "maDateClient": "+02:00"}

        soup  = self.httpUtils.jsonToSoup(self._siteRoot + "Commun/" + action + "/InitialiserDateClient", params)

        soup = self.httpUtils.urlToSoup(self._siteRoot + "Commun/" + action)

        return soup

    def listMessages(self, soup):
        actionUrl = self._siteRoot + "/Commun/MessagerieReception.aspx"
        params = None
        soup = self.httpUtils.urlToSoup(actionUrl, params)
        return soup

    def getNewMessages(self, soup):
        list = []
        newMessages = soup.find_all(class_=re.compile('message-nouveau'))
        print(newMessages)
        for msg in newMessages:
            url = msg.a['href']
            senderA = msg.find_all(id=re.compile('Expediteur'))
            sender = senderA[0].string
            subjectA = msg.find_all(id=re.compile('Objet'))
            subject = subjectA[0].string
            dateA = msg.find_all(id=re.compile('Date'))
            date = dateA[0].string
            list.append([url, sender, subject, date])
        return list


    def retrieveLastStatement(self, content):
        print("Retrieving")

scolInfo = ScolInfo(os.environ["HOME"], ##USER, ##PASS)
debug = True
soupNewSession = scolInfo.createSession()
soupLoggedIn = scolInfo.login(soupNewSession)
soupMessageList = scolInfo.listMessages(soupLoggedIn)
scolInfo.getNewMessages(soupMessageList)
