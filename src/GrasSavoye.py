#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os
from datetime import *
from BeautifulSoup import *

import HttpUtils
from RecupFactures import StatementRetriever

class GrasSavoye(StatementRetriever):
    _initialUrl = ""
    _siteRoot = ""
    _billUrl = ""

    def login(self, soup):
        print("Logging in")

    def retrieveLastStatement(self, content):
        print("Retrieving")

# https://extranet.grassavoye.com
# POST /LINA2/default.asp? HTTP/1.1
# USR_LOGIN	<user>
# USR_PASSWORD	<pass>
# idoubli
# Submit.x	52
# Submit.y	13
# Submit	Envoyer
