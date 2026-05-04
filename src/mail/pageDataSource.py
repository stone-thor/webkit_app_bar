#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  This file is part of Webkit App Bar.
#
#  Copyright 2011-2017 xDaks <http://xdaks.deviantart.com/>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

import sys, os, urllib, string
from PyQt4 import QtCore, QtGui, QtWebKit
import mail

def run(w, cmd):
    w.evaluateJavaScript(cmd)

def setData(Key, Val):
    return u'appData["{0}"] = "{1}";'.format(Key, Val)

class AccountData:
    """ returns the account name and password stored in >>account<< file """
    def __init__(self, browser):
        self.account = ''
        self.password = ''
        self.browser = browser
        self.getAccount()

    def getAccount(self):
        sLine = ''

        accountFile = self.browser.pageConfig['accountFile']
        accountFile = os.path.expanduser(accountFile)

        try:
            with open(accountFile) as f:
                sLine = f.readline()
        except:
            return

        sLine = string.replace(sLine, '\n', '')
        accValues = sLine.split(',')

        #print(accValues)
        if len(accValues) == 2:
            self.account = accValues[0]
            self.password = accValues[1]

class AppTimer:
    def __init__(self, browser):
        self.browser = browser
        self.Timer = None

    def _on_autoRefresh(self):
        self.browser.web_view.reload()

    def setAutoRefresh(self, interval):
        if self.Timer == None:
            self.Timer = QtCore.QTimer()
            self.Timer.timeout.connect(self._on_autoRefresh)
            self.Timer.start(interval * 1000)

aData = None
aTimer = None

def setAutoRefresh(browser, interval):
    global aTimer
    if aTimer == None:
        aTimer = AppTimer(browser)
        aTimer.setAutoRefresh(interval)

def getAccount(browser):
    global aData
    if aData == None:
        aData = AccountData(browser)
    return aData.account, aData.password

def init(browser):
    w = browser.web_view.page().mainFrame()
    print('pageDataSource init')

    run(w, 'appData = {};')

    account, password = getAccount(browser)
    if account != '' and password != '':
        nNewCount = mail.getNewCount(account, password, 'imap.gmail.com')
    else:
        nNewCount = '?'

    run(w, setData(u'NewCount', nNewCount))
    run(w, 'onInitData();')

    # refresh every 5 minutes
    #setAutoRefresh(browser, 300)
    setAutoRefresh(browser, 30)
