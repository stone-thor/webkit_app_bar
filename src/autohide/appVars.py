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

import sys, os, string, subprocess

xdgFolders = {'DOWNLOAD': '', 'PICTURES': '', 'DESKTOP': '', 'MUSIC': '', 'DOCUMENTS': '', 'VIDEOS': ''}
defaultApps = {'defaultBrowser': '', 'defaultFileManager': ''}

def initFolders():
    for key in xdgFolders:
        xdgFolders[key] = subprocess.check_output(['xdg-user-dir', key])
        #print(xdgFolders[key])

def initDefaultApps(browser):
    if 'defaultBrowser' in browser.pageConfig:
        defaultApps['defaultBrowser'] = browser.pageConfig['defaultBrowser']
    if 'defaultFileManager' in browser.pageConfig:
        defaultApps['defaultFileManager'] = browser.pageConfig['defaultFileManager']

def replaceCmdVars(cmd, varlist, var_prefix = ''):
    for key in varlist:
        val = varlist[key]
        if val != '':
            key = var_prefix + key
            if key in cmd:
                cmd = cmd.replace(key, val)
    return cmd

def OnCommand(cmd):
    print(__name__ + ' - OnCommand event')
    cmd = replaceCmdVars(cmd, defaultApps)
    cmd = replaceCmdVars(cmd, xdgFolders, '$XDG_')
    return cmd

def init(browser):
    # main - initialization plugin function - don't remove it
    browser.OnCommand = OnCommand
    initFolders()
    initDefaultApps(browser)