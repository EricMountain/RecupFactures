#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os
from datetime import *

import HttpUtils

# FIXME - Handle errors

# Slots management based on Linux Mag HS No 49 Juillet-Aout 2010
class AutoSlots(type):
    def __new__(cls, name, bases, attrs):
        slots = attrs.get('__slots__', set())
        if not bases: slots.add('__dict__')

        if attrs.get('_structure'):
            for p in attrs['_structure']:
                slots.add(p)

        attrs['__slots__'] = tuple(slots)

        return type.__new__(cls, name, bases, attrs)


class StatementRetriever(object):
    __metaclass__ = AutoSlots
    _structure = {'_siteRoot' : {'required' : True},
                  '_initialUrl' : {'required' : True},
                  'httpUtils' : {'required' : True},
                  'statementsPath' : {'required' : True},
                  'userid' : {'required' : True},
                  'password' : {'required' : True}}

    def __init__(self, statementsPath, userid, password):
        self.httpUtils = HttpUtils.HttpUtils()
        self.statementsPath = statementsPath
        self.userid = userid
        self.password = password

    def createSession(self):
        print("Establishing session to", self._initialUrl)

        soup = self.httpUtils.urlToSoup(self._initialUrl)

        return soup
