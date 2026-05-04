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

# example from - http://developer.yahoo.com/python/python-xml.html
# python weather wrapper: http://code.google.com/p/python-weather-api/

import urllib, string
from xml.dom import minidom

wCondEN = {
        "0": u"Tornado",
        "1": u"Tropical Storm",
        "2": u"Hurricane",
        "3": u"Severe Thunderstorms",
        "4": u"Thunderstorms",
        "5": u"Mixed Rain and Snow",
        "6": u"Mixed Rain and Sleet",
        "7": u"Mixed Precipitation",
        "8": u"Freezing Drizzle",
        "9": u"Drizzle",
        "10": u"Freezing Rain",
        "11": u"Light Rain",
        "12": u"Rain",
        "13": u"Snow Flurries",
        "14": u"Light Snow Showers",
        "15": u"Drifting Snow",
        "16": u"Snow",
        "17": u"Hail",
        "18": u"Sleet",
        "19": u"Dust",
        "20": u"Fog",
        "21": u"Haze",
        "22": u"Smoke",
        "23": u"Blustery",
        "24": u"Windy",
        "25": u"N/A",
        "26": u"Cloudy",
        "27": u"Mostly Cloudy",
        "28": u"Mostly Cloudy",
        "29": u"Partly Cloudy",
        "30": u"Partly Cloudy",
        "31": u"Clear",
        "32": u"Clear",
        "33": u"Fair",
        "34": u"Fair",
        "35": u"Mixed Rain and Hail",
        "36": u"Hot",
        "37": u"Isolated Thunderstorms",
        "38": u"Scattered Thunderstorms",
        "39": u"Scattered Showers",
        "40": u"Heavy Rain",
        "41": u"Scattered Snow Showers",
        "42": u"Heavy Snow",
        "43": u"Heavy Snow",
        "44": u"N/A",
        "45": u"Scattered Showers",
        "46": u"Snow Showers",
        "47": u"Isolated Thunderstorms",
        "na": u"N/A",
        "-" : u"N/A"
    }

wCondCZ = {
        "0": u"Tornádo",
        "1": u"Tropická bouře",
        "2": u"Hurikán",
        "3": u"Četné bouřky",
        "4": u"Bouřky",
        "5": u"Déšť se sněhem",
        "6": u"Déšť a plískanice",
        "7": u"Smíšené srážky",
        "8": u"Namrzající mrholení",
        "9": u"Mrholení",
        "10": u"Namrzající déšť",
        "11": u"Mírný déšť",
        "12": u"Déšť",
        "13": u"Sněhové přívaly",
        "14": u"Mírné sněžení",
        "15": u"Drifting Snow",
        "16": u"Sněžení",
        "17": u"Kroupy",
        "18": u"Plískanice",
        "19": u"Prašno",
        "20": u"Mlha",
        "21": u"Opar",
        "22": u"kouřmo",
        "23": u"Bouřlivě",
        "24": u"Větrno",
        "25": u"N/A",
        "26": u"Zataženo",
        "27": u"Oblačno",
        "28": u"Oblačno",
        "29": u"Polojasno",
        "30": u"Polojasno",
        "31": u"Jasno",
        "32": u"Jasno",
        "33": u"Pěkně",
        "34": u"Pěkně",
        "35": u"Déšť s kroupami",
        "36": u"Horko",
        "37": u"Osamocené bouřky",
        "38": u"Občasné bouřky",
        "39": u"Občasné přeháňky",
        "40": u"Hustý déšť",
        "41": u"Občasné sněžení",
        "42": u"Husté sněžení",
        "43": u"Husté sněžení",
        "44": u"N/A",
        "45": u"Občasné přeháňky",
        "46": u"Sněhové přeháňky",
        "47": u"Osamocené bouřky s deštěm",
        "na": u"N/A",
        "-" : u"N/A"
    }

wDaysCZ = {
    "Mon" : u"Pondělí",
    "Tue" : u"Úterý",
    "Wed" : u"Středa",
    "Thu" : u"Čtvrtek",
    "Fri" : u"Pátek",
    "Sat" : u"Sobota",
    "Sun" : u"Neděle"
    }

wMonthNum = {
    "Jan": "1",
    "Feb": "2",
    "Mar": "3",
    "Apr": "4",
    "May": "5",
    "Jun": "6",
    "Jul": "7",
    "Aug": "8",
    "Sep": "9",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
    }


def translate(val, dict):
    """translace value"""
    return dict.get(val, val)

def getDate(val, dict):
    """translate date"""
    for d in dict:
        if d in val:
            date = val.replace(d, dict.get(d))
            return date.replace(' ', '.')

def getForecast(code):
    """get forecast data from url"""
    WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'
    # 5 days forecast in celsius
    WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss/{0}_c.xml'

    url = WEATHER_URL.format(code)
    xml = urllib.urlopen(url)
    dom = minidom.parse(xml)

    forecasts = []
    cond = ''
    day = ''
    date = ''
    #for node in dom.getElementsByTagNameNS(WEATHER_NS, 'astronomy'):
        #print(node.getAttribute('sunrise'))
        #print(node.getAttribute('sunset'))

    for node in dom.getElementsByTagNameNS(WEATHER_NS, 'forecast'):
        # czech translation
        #~ code = node.getAttribute('code')
        #~ cond =  translate(code, wCondCZ)
        #~ day =   translate(node.getAttribute('day'), wDaysCZ)
        #~ date =  getDate(node.getAttribute('date'), wMonthNum)

        code =  node.getAttribute('code')
        cond =  translate(code, wCondEN)
        day =   node.getAttribute('day')
        date =  getDate(node.getAttribute('date'), wMonthNum)

        forecasts.append({
            'day': day,
            'date': date,
            'low': node.getAttribute('low'),
            'high': node.getAttribute('high'),
            'condition': cond,
            'code': code
        })

    return forecasts

def main():
    wForecast = getForecast('EZXX0002')
    s = '''W E A T H E R${alignr}Brno
    ${voffset -20}
    ${hr}'''.encode("utf-8")
    print(s)
    for day in wForecast:
        #s = u'{0[day]} {0[date]} {0[high]}/{0[low]} °C {0[condition]}'.format(day)
        s = u'{0[day]}: ${{alignr}} {0[condition]}'.format(day)
        print(s.encode("utf-8"))
        s = u'${{alignr}}{0[high]} / {0[low]} °C'.format(day)
        print(s.encode("utf-8"))

    return 0

if __name__ == '__main__':
    main()
