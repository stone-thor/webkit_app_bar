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

import sys, os, urllib, string, signal
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtCore import Qt, QUrl
from PyQt4.QtGui import QApplication, QPalette
from subprocess import Popen

# -------------------------------------------------------------------- #
# globals
# -------------------------------------------------------------------- #
appName = 'webkitAppBar'
appPath = os.path.dirname(os.path.realpath( __file__ ))
#appWorkDir = 'logout_new'
appWorkDir = ''
appFile = os.path.join(appWorkDir, 'index.html')
defaultSite = os.path.join(appPath, appFile)

class Events(QtCore.QObject):
    execCmd = QtCore.pyqtSignal(object)
    windowShow = QtCore.pyqtSignal(object)

class Browser():

    # ---------------------------------------------------------------- #
    # events - BEGIN
    # ---------------------------------------------------------------- #

    # event -  onLinkCliked
    def _on_navigation(self, url):
        url = str(url.toString().toUtf8())
        if self.on_command(url):
            return True
        else:
            #self.web_view.load(QUrl(url))
            return False

    # event -  onCompletePageLoading
    def _on_pageLoaded(self, ok):
        try:
            self.pageConfig = self.getConfig()
            l, t, w, h = self.getBarDimension()
            print(l, t, w, h)

            self.window.setGeometry(l, t, w, h)
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
        return

        try:
            import plugins
            try:
                plugins.init(self)
            except:
                print('plugins init error')
        except:
            pass

    def getConfig(self):
        # convert - Qt types to  Python types
        result = {}
        cfg = self.getVar(self.web_view, 'config')
        for key in cfg:
            Val = cfg[key]
            if type(Val) == QtCore.QString:
                Val = str(Val)
            result[str(key)] = Val
        return result

    def normalizeCmd(self, cmd):
        cmd = cmd.replace('cmd::', '')
        cmd = urllib.unquote_plus(cmd)
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
            return web_view.page().mainFrame().evaluateJavaScript(varName).toPyObject()
        except:
            pass

    def getBarDimension(self):
        top = self.pageConfig['Top']
        left = self.pageConfig['Left']
        width = self.pageConfig['Width']
        height = self.pageConfig['Height']
        return int(left), int(top), int(width), int(height)

    def getDesktop(self):
        try:
            curDesktop = os.environ['XDG_CURRENT_DESKTOP']
        except:
            curDesktop = ''

        try:
            wmName = os.environ['DESKTOP_SESSION']
        except:
            wmName = 'unknown'

        return curDesktop.lower() if curDesktop != '' else wmName.lower()

    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)

        self.Events = Events()

        print(defaultSite)
        self.default_site = defaultSite
        self.appWorkDir = appWorkDir

        self.window = QtGui.QMainWindow()
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

        self.web_view = QtWebKit.QWebView()

        # transparent webview
        palette = self.web_view.palette()
        palette.setBrush(QPalette.Base, Qt.transparent)
        self.web_view.page().setPalette(palette)
        self.web_view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.web_view.loadFinished.connect(self._on_pageLoaded)
        self.web_view.linkClicked.connect(self._on_navigation)

        self.window.setCentralWidget(self.web_view)
        self.web_view.load(QUrl(self.default_site.decode("utf-8")))

    def main(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        sys.exit(self.app.exec_())

def readCmdLine():
    if len(sys.argv) > 1:
        try:
            DirName = sys.argv[1]

            FileName = ''
            fName = os.path.join(appPath, DirName, appFile)
            if os.path.isfile(fName):
                FileName = fName

            #print(FileName)
            if FileName != '':
                global defaultSite
                defaultSite = FileName

            if DirName != None:
                global appWorkDir
                appWorkDir = DirName

        except:
            print('read html source file error')
    else:
        print('no source file...')

readCmdLine()
browser = Browser()
browser.main()