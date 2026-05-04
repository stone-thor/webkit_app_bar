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
import weather

def run(w, cmd):
    w.evaluateJavaScript(cmd)

def getDay(wForecast, day):
    return wForecast[day - 1]

def setData(Key, Val):
    return u'appData["{0}"] = "{1}";'.format(Key, Val)

def setDayData(w, wForecast, DayNum):
    D = getDay(wForecast, DayNum)
    D['day'] = D['day'][:2]                                     # create day shortcut
    D['date'] = '{0[0]}.{0[1]}.'.format(D['date'].split('.'))   # delete year from date

    day  =  "Day{0}".format(DayNum)
    date = "Date{0}".format(DayNum)
    low  =  "Low{0}".format(DayNum)
    high = "High{0}".format(DayNum)
    cond = "Cond{0}".format(DayNum)
    code = "Code{0}".format(DayNum)

    run(w, setData(day,  D['day']))
    run(w, setData(date, D['date']))
    run(w, setData(low,  D['low']))
    run(w, setData(high, D['high']))
    run(w, setData(cond, D['condition']))
    run(w, setData(code, D['code']))

def init(browser):
    w = browser.web_view.page().mainFrame()
    print('pageDataSource init')

    run(w, 'appData = {};')
    # ---------------------------------------------------------------- #
    # replace USNY0996 (New York, United States) with your city code
    # check it out on http://edg3.co.uk/snippets/weather-location-codes/
    wForecast = weather.getForecast('EZXX0002')

    for i in range(1,6):
        setDayData(w, wForecast, i)
    # ---------------------------------------------------------------- #
    run(w, 'onInitData();')
