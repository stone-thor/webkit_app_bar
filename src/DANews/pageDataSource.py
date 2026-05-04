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
from PyQt4.QtCore import Qt, QUrl
from PyQt4.QtGui import QApplication, QPalette
import rss

def jsExec(w, cmd):
    w.page().mainFrame().evaluateJavaScript(cmd)

def initData(w):
    jsExec(w, u'appData = {};')

def setData(w, key, val):
    cmd = u'appData["{0}"] = "{1}";'.format(key, val)
    jsExec(w, cmd)

def setCount(w, val):
    cmd = u'appData.Count = "{0}";'.format(val)
    jsExec(w, cmd)

def init(browser):
    # entry point to initialize page data
    print('pageDataSource init')
    w = browser.web_view
    initData(w)
    data = rss.getData('customization/screenshots/nix', 10)
    ID = 1
    for i in data:
        #print(ID)
        setData(w, u'Title' + str(ID), i['title'])
        setData(w, u'Author' + str(ID), '~' + i['author'])
        setData(w, u'ThumbUrl' + str(ID), i['thumb-url'])
        setData(w, u'Link' + str(ID), i['link'])
        ID += 1

    setCount(w, len(data))
    jsExec(w, 'onInitData();')
