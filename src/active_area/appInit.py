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

import sys, os, string, time
import PyQt5
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QApplication
from subprocess import Popen

class appObject:
    def __init__(self, browser):
        #print(dir(browser.web_view))
        self.browser = browser
        browser.web_view.enterEvent = self.onEnter
        browser.web_view.leaveEvent = self.onLeave

        l, t, w, h = self.browser.getBarDimension()

        self.onEnterCommand = ''
        if 'onEnter' in browser.pageConfig:
            self.onEnterCommand = browser.pageConfig['onEnter']

        self.onLeaveCommand = ''
        if 'onLeave' in browser.pageConfig:
            self.onLeaveCommand = browser.pageConfig['onLeave']

    def setStateColor(self, Visible):
        m = self.browser.web_view.page().mainFrame()
        if Visible:
            m.evaluateJavaScript('setShowColor();')
        else:
            m.evaluateJavaScript('setHideColor();')

    def onEnter(self, evt):
        self.setStateColor(True)
        if self.onEnterCommand != '':
            Popen(self.onEnterCommand, shell=True)

    def onLeave(self, evt):
        self.setStateColor(False)
        if self.onLeaveCommand != '':
            Popen(self.onLeaveCommand, shell=True)

appObj = None

def init(browser):
    #change main window attributes to >>stay on top dock<<
    browser.window.setAttribute(Qt.WA_X11NetWmWindowTypeDesktop, False)
    browser.window.setAttribute(Qt.WA_X11NetWmWindowTypeDock, True)
    browser.window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)

    global appObj
    if appObj == None:
        appObj = appObject(browser)

    appObj.setStateColor(False)