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
from subprocess import Popen

class javascriptObject(QtCore.QObject):
    @QtCore.pyqtSlot(str)
    def command(self, cmd):
        self.browser._on_navigation(QUrl(cmd))

    def _pyVersion(self):
        return sys.version

    def __del__(self):
        print('javascriptObject destroy')

    pyVersion = QtCore.pyqtProperty(str, fget=_pyVersion)

jsObj = None

def init(browser):
    # create >>app<< object callable from javascript
    m = browser.web_view.page().mainFrame()

    global jsObj
    if jsObj != None:
        jsObj.deleteLater()

    jsObj = javascriptObject()
    jsObj.browser = browser
    m.addToJavaScriptWindowObject("app", jsObj)
    print('jsObject init')

