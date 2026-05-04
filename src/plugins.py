#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  This file is part of Webkit App Bar.
#
#  Copyright 2011-2014 xDaks <http://xdaks.deviantart.com/>
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
import types
import Global

def loadPluginList(browser):
    pluginList = []

    if not 'plugin' in browser.pageConfig: return pluginList
    plugin = browser.pageConfig['plugin']

    if type(plugin) == str:
        if browser.appWorkDir != '':
            plugin = '.'.join ([browser.appWorkDir, plugin])
        pluginList.append(plugin)

    elif type(plugin) is list:
        for val in plugin:
            if browser.appWorkDir != '':
                val = '.'.join ([browser.appWorkDir, val])
            pluginList.append(val)

    return pluginList

def init(browser):
    sys.path.insert(1, os.path.join(Global.appPath, browser.appWorkDir))

    pluginList = loadPluginList(browser)
    print(pluginList)

    for plugin in pluginList:
        print(plugin)
        exec('import ' + plugin)
        sys.modules[plugin].init(browser)
