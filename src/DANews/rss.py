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

from urllib import request
from xml.dom import minidom

def nodeValue(e):
    return " ".join(t.nodeValue for t in e.childNodes if t.nodeType == t.TEXT_NODE)

def getData(category, max_count):
    if category == '':
        category = 'customization/screenshots/nix'
    #category = 'customization/icons/dock'
    #category = 'customization/skins/linuxutil'
    URL = 'http://backend.deviantart.com/rss.xml?q=in%3A' + category + '+sort%3Atime'
    print(URL)
    data = []
    index = 0
    dom = minidom.parse(request.urlopen(URL))

    for node in dom.getElementsByTagName('item'):
        i = node.getElementsByTagName('title')[0]
        title = nodeValue(i)

        i = node.getElementsByTagName('media:credit')[0]
        author = nodeValue(i)

        i = node.getElementsByTagName('media:thumbnail')[0]
        thumb_url = i.getAttribute('url')

        i = node.getElementsByTagName('link')[0]
        link = nodeValue(i)

        data.append({'title': title,
                     'author': author,
                     'thumb-url': thumb_url,
                     'link': link
        })
        index += 1
        if index >= max_count:
            break

    return data

def main():
    data = getData('customization/skins/linuxutil', 10)
    for i in data:
        print(u'Title: {0[title]}, Author: {0[author]}'.format(i))

if __name__ == '__main__':
    main()
