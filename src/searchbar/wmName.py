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

from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtCore import Qt, QUrl
from PyQt4.QtGui import QApplication, QPalette
from Xlib.display import Display
from Xlib import X

def setWMClass(winId, name, className):
    display = Display()
    window = display.create_resource_object('window', winId)
    window.set_wm_class(name, className)
    print(window.get_wm_class())

def init(browser):
    # get mainwindow ID and set application (class) name
    winId = browser.window.winId()

    appName = ''
    if 'appName' in browser.pageConfig:
        appName = browser.pageConfig['appName']
    else:
        appName = browser.appWorkDir

    if appName != '':
        setWMClass(winId, appName, appName)

    print('wmName init')