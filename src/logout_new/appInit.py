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

import sys, os, string, subprocess, time
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtCore import Qt, QUrl
from PyQt4.QtGui import QApplication, QPalette
from Xlib import X, display, protocol, Xatom
import Xlib.protocol.event

atoms = {
    'type_desktop' : '_NET_WM_WINDOW_TYPE_DESKTOP',
    'type_dock'    : '_NET_WM_WINDOW_TYPE_DOCK',
    'type_normal'  : '_NET_WM_WINDOW_TYPE_NORMAL',
    'win_type'     : '_NET_WM_WINDOW_TYPE',
    'state_below'  : '_NET_WM_STATE_BELOW',
    'state_above'  : '_NET_WM_STATE_ABOVE',
    'skip_taskbar' : '_NET_WM_STATE_SKIP_TASKBAR',
    'wm_state'     : '_NET_WM_STATE',
    'wm_check'     : '_NET_SUPPORTING_WM_CHECK',
    'wm_name'      : '_NET_WM_NAME',
    'client_list'  : '_NET_CLIENT_LIST'
}
class X11WinManager(QtCore.QThread):
    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window
        self.display = display.Display()
        self.root = self.display.screen().root
        self.win = self.display.create_resource_object("window", int(self.window.winId()))
        self.root.change_attributes(event_mask=(X.PropertyChangeMask|X.ExposureMask|X.StructureNotifyMask|X.VisibilityChangeMask))
        self.display.flush()

    def sendEvent(self, win, ctype, data, mask=None):
        data = (data+[0]*(5-len(data)))[:5]
        ev = Xlib.protocol.event.ClientMessage(window=win, client_type=ctype, data=(32,(data)))
        if not mask:
            mask = (X.SubstructureRedirectMask or X.SubstructureNotifyMask)
        self.root.send_event(ev, event_mask=mask)

    def atom(self, name):
        return self.display.intern_atom(atoms.get(name, name))

    def setSkipTaskbar(self):
        #data = [1, self.atom('state_above')]
        data = [1, self.atom('skip_taskbar')]
        self.sendEvent(self.win, self.atom('wm_state'), data)
        self.display.flush()
        #print('setAbove')

    def run(self):
            while 1:
                attr = self.win.get_attributes()
                if attr.map_state == X.IsViewable:
                    #print('X11WinManager is viewable...')
                    self.setSkipTaskbar()
                    break
                else:
                    pass
                    #print('X11WinManager is NOT viewable...')
                time.sleep(0.1)

def center(window):
    qr = window.frameGeometry()
    cp = QtGui.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())


def init(browser):
    #change main window attributes to 'stay on top'

    browser.window.setAttribute(Qt.WA_X11NetWmWindowTypeDesktop, False)
    #browser.window.setAttribute(Qt.WA_X11NetWmWindowTypeDock, True)
    browser.window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    #browser.window.setWindowFlags(Qt.X11BypassWindowManagerHint)
    center(browser.window)

    #global man
    #man = X11WinManager(browser.window)
    #man.start()

    print('appInit')

