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

from Xlib import display, X, Xatom
import sys, time
from PyQt4 import QtCore

#class Atom:
    #_list_ = {
            #'ACTIVE_WINDOW' :  '_NET_ACTIVE_WINDOW',
            #'FRAME_EXTENTS' :  '_NET_FRAME_EXTENTS',
            #'WINDOW_TYPE'   :  '_NET_WM_WINDOW_TYPE',
            #'TYPE_DESKTOP'  :  '_NET_WM_WINDOW_TYPE_DESKTOP',
            #'TYPE_DOCK'     :  '_NET_WM_WINDOW_TYPE_DOCK',
            #'TYPE_UTILITY'  :  '_NET_WM_WINDOW_TYPE_UTILITY',
            #'TYPE_NORMAL'   :  '_NET_WM_WINDOW_TYPE_NORMAL',
            #'CLIENT_LIST'   :  '_NET_CLIENT_LIST'
    #}
    #Display = display.Display()
    #for key, val in _list_.items():
        #vars()[key] = Display.get_atom(val)

# How do you programmatically set an attribute
# http://stackoverflow.com/a/285076

# How do I call setattr() on the current module
# http://stackoverflow.com/a/2933481

# Setting an class attribute with a given name in python while defining the class
# http://stackoverflow.com/a/20608050

class Atoms:
    def __init__(self):
        self.display = display.Display()
        self.ACTIVE_WINDOW = self.atom('_NET_ACTIVE_WINDOW')
        self.FRAME_EXTENTS = self.atom('_NET_FRAME_EXTENTS')
        self.WINDOW_TYPE   = self.atom('_NET_WM_WINDOW_TYPE')
        self.TYPE_DESKTOP  = self.atom('_NET_WM_WINDOW_TYPE_DESKTOP')
        self.TYPE_DOCK     = self.atom('_NET_WM_WINDOW_TYPE_DOCK')
        self.TYPE_UTILITY  = self.atom('_NET_WM_WINDOW_TYPE_UTILITY')
        self.TYPE_NORMAL   = self.atom('_NET_WM_WINDOW_TYPE_NORMAL')
        self.CLIENT_LIST   = self.atom('_NET_CLIENT_LIST')

    def atom(self, value):
        return self.display.get_atom(value)

Atom = Atoms()

class HideManager(QtCore.QThread):
    state_changed = QtCore.pyqtSignal(object)

    def __init__(self, appObject):
        QtCore.QThread.__init__(self)

        self.appRect = appObject.showRect
        self.multiWinClass = appObject.multiWinClass()

        self.display = display.Display()
        self.root = self.display.screen().root
        self.root.change_attributes(event_mask=(X.PropertyChangeMask))
        self.display.flush()

    def isDock(self, win):
        prop = win.get_full_property(Atom.WINDOW_TYPE, 0)
        if prop and (Atom.TYPE_DESKTOP in prop.value or Atom.TYPE_DOCK in prop.value):
            return True
        return False

    def isMainWindow(self, win):
        prop = win.get_full_property(Atom.WINDOW_TYPE, 0)
        if prop and (Atom.TYPE_NORMAL in prop.value):
            return True
        return False

    def isToolWindow(self, win):
        prop = win.get_full_property(Atom.WINDOW_TYPE, 0)
        if prop and (Atom.TYPE_UTILITY in prop.value):
            return True
        return False

    def getClass(self, win):
        name = win.get_wm_class()
        if name and type(name) is tuple:
            return name[0].lower()
        return ''

    def getWinGroup(self, grpwin):
        result = []
        result.append(grpwin)
        cls_name = self.getClass(grpwin)
        tasks = self.root.get_full_property(Atom.CLIENT_LIST, Xatom.WINDOW).value
        for task in tasks:
            win = self.display.create_resource_object("window", task)
            if self.getClass(win) == cls_name and win.id != grpwin.id:
                attr = win.get_attributes()
                if attr.map_state == X.IsViewable:
                    result.append(win)
        return result

    def getGeometry(self, win):
        frame = win.get_full_property(Atom.FRAME_EXTENTS, 0)
        f0, f1, f2, f3 = int(frame.value[0]), int(frame.value[1]), int(frame.value[2]), int(frame.value[3])
        geom = win.get_geometry()
        trans_geom = win.translate_coords(self.root, geom.x, geom.y)
        x, y = trans_geom.x * -1, trans_geom.y * -1
        w, h = geom.width + f0 + f1, geom.height + f2 + f3
        return QtCore.QRect(x, y, w, h)

    def intersectGroup(self, win):
        tools = self.getWinGroup(win)
        for tool in tools:
            if self.appRect.intersects(self.getGeometry(tool)):
                return True
        return False

    def intersects(self, win):
        if self.getClass(win) in self.multiWinClass:
            return self.intersectGroup(win)
        else:
            return self.appRect.intersects(self.getGeometry(win))

    def checkActiveWindow(self):
        active = self.root.get_full_property(Atom.ACTIVE_WINDOW, 0)
        if (not active) or (active.value[0] == 0):
            self.state_changed.emit(True)
            return
        try:
            win = self.display.create_resource_object("window", active.value[0])
            attr = win.get_attributes()
            if attr.map_state == X.IsViewable:
                visible = self.isDock(win) or not self.intersects(win)
                self.state_changed.emit(visible)
        except:
            pass

    def run(self):
        while 1:
            self.checkActiveWindow()
            time.sleep(0.2)