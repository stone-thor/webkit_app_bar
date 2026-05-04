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

import sys, os, string, time, types
import PyQt5
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QApplication
import X11hidemanager

class appObject:
    def __init__(self, browser, visibleLen, animate):
        #print(dir(browser.web_view))
        self.browser = browser
        browser.web_view.enterEvent = self.onEnter
        browser.web_view.leaveEvent = self.onLeave
        browser.Events.execCmd.connect(self.onExec)

        self.intellihide = self.getIntellihide()
        self.initState()

        self.Animate = animate
        l, t, w, h = self.browser.getBarDimension()
        self.showRect = QtCore.QRect(l, t, w, h)
        self.hideRect = QtCore.QRect((w - visibleLen) * -1, t, w, h)

        #fix -> hides scrollbars during the animation
        browser.web_view.setFixedSize(w, h)

        if self.intellihide:
            self.hidemanager = X11hidemanager.HideManager(self)
            self.hidemanager.state_changed.connect(self.onStateChanged)
            self.hidemanager.start()
        else:
            self.doHide()

    def getIntellihide(self):
        cfg_val = self.browser.pageConfig['intellihide']
        return (type(cfg_val) == bool) and cfg_val

    def multiWinClass(self):
        result = []
        cfg_val = self.browser.pageConfig['multiWinClass']
        if cfg_val and type(cfg_val) is list:
            for val in cfg_val:
                result.append(str(val))
        return result

    def onExec(self, cmd):
        if not self.intellihide:
            return
        print('appObject.onExec')
        self.initState()
        self.Execute = True

    def initState(self):
        self.Visible = self.intellihide #True
        self.StateChanging = False
        self.manVisible = self.intellihide #True
        self.MouseVisible = False
        self.Execute = False

    def onStateChanged(self, visible):
        #print('appObject.on_state_changed', visible)
        self.doChange(visible)

    def setStateColor(self, Visible):
        m = self.browser.web_view.page().mainFrame()
        if Visible:
            m.evaluateJavaScript('setShowColor();')
        else:
            m.evaluateJavaScript('setHideColor();')

    def onEnter(self, evt):
        #print(self.manVisible, self.Visible)
        if not self.manVisible and not self.Visible:
            self.StateChanging = True
            self.doShow()
            self.MouseVisible = True
            self.StateChanging = False

    def onLeave(self, evt):
        if not self.manVisible and self.Visible:
            self.StateChanging = True
            self.doHide()
            self.MouseVisible = False
            self.StateChanging = False

    def doChange(self, visible):
        if self.Execute or self.MouseVisible or visible == self.Visible or self.StateChanging:
            self.Execute = False
            return

        self.StateChanging = True
        self.manVisible = visible
        if visible:
            self.doShow()
        else:
            self.doHide()
        self.StateChanging = False

    def doShow(self):
        self.Visible = True
        if self.Animate:
            self.doAnimate(self.hideRect, self.showRect)
        else:
            self.browser.window.setGeometry(self.showRect)

        self.setStateColor(True)

    def doHide(self):
        self.Visible = False
        if self.Animate:
            self.doAnimate(self.showRect, self.hideRect)
        else:
            self.browser.window.setGeometry(self.hideRect)

        self.setStateColor(False)

    def doAnimate(self, startRect, endRect):
        ani = QtCore.QPropertyAnimation(self.browser.window, b"geometry", self.browser.window)
        ani.setDuration(250)
        ani.setStartValue(startRect)
        ani.setEndValue(endRect)
        ani.start()

appObj = None

def init(browser):
    #change main window attributes to >>stay on top dock<<
    browser.window.setAttribute(Qt.WA_X11NetWmWindowTypeDesktop, False)
    browser.window.setAttribute(Qt.WA_X11NetWmWindowTypeDock, True)
    browser.window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)

    global appObj
    if appObj == None:
        appObj = appObject(browser, 6, True)
