Webkit App Bar - Qt5 version
----------------------------
Is kind of "desktop widget" written in Python 3 with using QtWebKit.
Works same way as Qt4 version (no interface changing).
Intended for distros, which removed Qt4 webkit support, beginning with Debian 9, *buntu 17.10, Manjaro 17.* ... and newer.

Requirements
-------------
Distro with Qt5 of version at least 5.6 is required, because of missing WA_X11NetWmWindowType attributes in older version: https://codereview.qt-project.org/#/c/111936/
In Debian based distros install Python 3 & PyQt 5:
sudo apt-get install python3 python3-pyqt5 python3-pyqt5.qtwebkit

How to check Qt5 version
------------------------
In terminal run:
python3 qBrowser.py --info

How to use it
-------------
Run app bar:
python3 qBrowser.py appbar
or simplest bar version (just single html file):
python3 qBrowser.py appbar_simple

Run autohide app bar:
python3 qBrowser.py autohide
Note: required Xlib: sudo apt-get install python3-xlib

Run deviantArt RSS widget:
python3 qBrowser.py DANews

Run OpenBox logout dialog:
python3 qBrowser.py logout
or
python3 qBrowser.py logout_new

Run gMail widget:
python3 qBrowser.py mail
Note: put your gmail account name and password into ~/.gaccount file in format <account>, <password> e.g.: richard-johnson@gmail.com, rich911

Run search bar widget:
python3 qBrowser.py searchbar

Run active area widget:
python3 qBrowser.py active_area
Note: required xdotool: sudo apt-get install xdotool

Run tiles dialog:
python3 qBrowser.py tiles

Customization
-------------
Change *.html, *.css or any file you want :-)

enjoy!
http://xdaks.deviantart.com
