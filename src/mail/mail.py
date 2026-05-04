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

import imaplib

def getNewCount(username, password, mailserver, port = 993):
    # connect to email's server (uses SSL)
    server = imaplib.IMAP4_SSL(mailserver, port)

    try:
        # login with the variables provided up top
        server.login(username, password)
        try:
            mailbox = 'INBOX'
            # select your mailbox
            server.select(mailbox)

            # pull info for that mailbox
            data = str(server.status(mailbox, '(MESSAGES UNSEEN)'))
            tokens = data.split()

            # unread messages
            nCount = tokens[5].replace(')\'])','')

        finally:
            # close the mailbox
            server.close()
            # logout of the server
            server.logout()
    except:
        return 'err'

    return nCount
