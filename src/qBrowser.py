#!/usr/bin/env python3
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

import sys
import os
import urllib.parse
import string
import signal
import Global

import PyQt5
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5 import QtWebKit

from subprocess import Popen

print('PYQT_VERSION:', PyQt5.QtCore.PYQT_VERSION_STR)
print('WebKit Version: ', QtWebKit.qWebKitVersion())

# -------------------------------------------------------------------- #
# globals
# -------------------------------------------------------------------- #
appName = 'webkitAppBar'
appPath = os.path.dirname(os.path.realpath( __file__ ))

class APP:
    WorkDir = ''
    #WorkDir = 'DANews'          # Qt5 OK
    #WorkDir = 'weather'         # not working
    #WorkDir = 'logout'          # Qt5 OK
    #WorkDir = 'searchbar'       # Qt5 OK
    #WorkDir = 'mail'            # Qt5 OK
    #WorkDir = 'autohide'        # Qt5 OK
    #WorkDir = 'appbar'          # Qt5 OK
    #WorkDir = 'appbar_simple'   # Qt5 OK
    #WorkDir = 'empty'           # Qt5 OK
    #WorkDir = 'clock'           # Qt5 OK
    #WorkDir = 'clock_old'       # Qt5 OK
    #WorkDir = 'active_area'     # Qt5 OK
    File = ''
    DefaultSite = ''

def initAPP(workdir = APP.WorkDir):
    APP.WorkDir = workdir
    APP.File = os.path.join(APP.WorkDir, 'index.html')
    APP.DefaultSite = os.path.join(appPath, APP.File)

initAPP()

class Events(QtCore.QObject):
    execCmd = QtCore.pyqtSignal(object)
    windowShow = QtCore.pyqtSignal(object)

class MyMainWindow(QMainWindow):

    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.browser = None
        self.inspector = None

    def initInspector(self, browser):
        import appInspector
        self.browser = browser
        self.inspector = appInspector.Inspector(browser)

    def changeEvent(self, args):
        #print('changeEvent')
        self.lower()

    def showEvent(self, args):
        if self.inspector:
            self.inspector.Visible(True)

    #def enterEvent(self, args):
        #print('enterEvent')

    #def actionEvent(self, args):
        #print('actionEvent')

    #def windowStateChangeEvent(self, args):
        #print('WindowStateChangeEvent')

    #def event(self, event):
        ##print('event', event.Type)
        #return True

class Browser:
    # ---------------------------------------------------------------- #
    # events - BEGIN
    # ---------------------------------------------------------------- #

    # event - onLinkCliked
    def _on_navigation(self, url):
        url = str(url.toString())
        if self.on_command(url):
            return True
        else:
            #self.web_view.load(QUrl(url))
            return False

    # event - onCompletePageLoading
    def _on_pageLoaded(self, ok):
        try:
            self.pageConfig = self.getConfig()
            geometry = self.getBarDimension()
            print('PageLoaded: ', ok)

            self.window.setGeometry(*geometry)
        except:
            raise

        self.initPlugins()
        self.window.show()
        self.Events.windowShow.emit(self.window)

    # ---------------------------------------------------------------- #
    # events - END
    # ---------------------------------------------------------------- #

    def initPlugins(self):
        import plugins
        plugins.init(self)

    def getConfig(self):
        return self.getVar(self.web_view, 'config')

    def normalizeCmd(self, cmd):
        cmd = cmd.replace('cmd::', '')
        cmd = urllib.parse.unquote_plus(cmd)
        cmd = os.path.expandvars(cmd)
        return cmd

    def doCommandEvent(self, cmd):
        # call OnCommand event, if was created in plugin...
        event_name = 'OnCommand'
        if hasattr(self, event_name) and callable(getattr(self, event_name)):
            return self.OnCommand(cmd)
        return cmd

    def on_command(self, cmd):
        if cmd.startswith('cmd::'):
            cmd = self.normalizeCmd(cmd)
            cmd = self.doCommandEvent(cmd)

            print(cmd)

            if (cmd == 'exit'):
                sys.exit()
            elif (cmd == 'refresh'):
                self.web_view.reload()
            else:
                Popen(cmd, shell=True)
                self.Events.execCmd.emit(cmd)

            return True
        else:
            return False

    def getVar(self, web_view, varName):
        try:
            return web_view.page().mainFrame().evaluateJavaScript(varName)
        except:
            pass

    def getBarDimension(self):
        return (self.pageConfig.get('Left', 0),
                self.pageConfig.get('Top', 0),
                self.pageConfig.get('Width', 0),
                self.pageConfig.get('Height', 0))

    def getDesktop(self):
        return (os.environ.get('XDG_CURRENT_DESKTOP') or
                os.environ.get('DESKTOP_SESSION') or
                '').lower()

    def _on_Activate(self):
        print('_on_Activate')


    def __init__(self):
        self.appWorkDir = APP.WorkDir

        self.Events = Events()

        self.window = MyMainWindow()

        # ------------------------------------------------------------ #
        desktop = self.getDesktop()
        print(desktop)

        # windowAttribute for openbox/pekwm WM
        if desktop in ['unknown', 'openbox', 'pekwm']:
            self.window.setAttribute(Qt.WA_X11NetWmWindowTypeDesktop)
        # windowAttribute for any other DE like xfce, gnome, unity ...
        else:
            self.window.setAttribute(Qt.WA_X11NetWmWindowTypeDock)
            self.window.setWindowFlags(Qt.WindowStaysOnBottomHint)

        self.window.setAttribute(Qt.WA_TranslucentBackground)
        # ------------------------------------------------------------ #

        # DEBUG SETTING FOR *buntu & Mint
        # ============================================================ #
        if Global.desktop_debug:
            self.window.setAttribute(Qt.WA_TranslucentBackground or Qt.WA_X11NetWmWindowTypeDesktop)
            self.window.setWindowFlags(Qt.FramelessWindowHint or Qt.WindowStaysOnBottomHint or Qt.BypassWindowManagerHint)
        # ============================================================ #

        self.web_view = QWebView(self.window)

        # trasparent webview
        palette = self.web_view.palette()
        palette.setBrush(QPalette.Base, Qt.transparent)
        self.web_view.page().setPalette(palette)
        self.web_view.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.web_view.loadFinished.connect(self._on_pageLoaded)
        self.web_view.linkClicked.connect(self._on_navigation)

        self.window.setCentralWidget(self.web_view)
        self.web_view.load(QUrl('file://' + APP.DefaultSite))

        if Global.debug:
            self.window.initInspector(self)

def readCmdLine():
    if len(sys.argv) > 1:
        try:
            initAPP(sys.argv[1])
            if not os.path.isfile(APP.File):
                raise
        except:
            print('read html source file error')
            return False
    else:
        print('no source file...')

    return True

if __name__ == '__main__':
    if '--info' in sys.argv:
        sys.exit()

    Global.appPath = appPath
    Global.debug = (os.environ.get('WEBKIT_APP_BAR') or '').lower() == 'debug'
    Global.desktop_debug = (os.environ.get('WEBKIT_APP_BAR_DESKTOP') or '').lower() == 'debug'

    if not readCmdLine():
        sys.exit()

    app = QApplication(sys.argv)
    app.setApplicationName('qBrowser5')  # class setting -> second element of window's WM_CLASS property (see xprop)

    browser = Browser()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())