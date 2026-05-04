Webkit App Bar - Qt4 version
----------------------------
Is kind of "desktop widget" written in Python 2 with using QtWebKit.
Intended for a little bit older distros like Debian 8, *buntu 16.04 LTS, Mint 18.* .

Requirements
-------------
In Debian based (CrunchBang, *buntu, Mint...) distro install Python + PyQt:
sudo apt-get install python python-qt4

How to use it
-------------
Run app bar:
python qBrowser.py appbar
or simplest bar version (just single html file):
python qBrowser.py appbar_simple

Run autohide app bar:
python qBrowser.py autohide

Run deviantArt RSS widget:
python qBrowser.py DANews

Run OpenBox logout dialog:
python qBrowser.py logout

Run gMail widget:
python qBrowser.py mail
Note: put your gmail account name and password into ~/.gaccount file in format <account>, <password> e.g.: richard-johnson@gmail.com, rich911

Run search bar widget:
python qBrowser.py searchbar

Run weather widget:
python qBrowser.py weather
Note: by default widget shows weather in New York, you can change your city code in weather/pageDataSource.py - check out the instructions in the file

Run active area widget:
python qBrowser.py active_area
Note: required xdotool

Customization
-------------
Change *.html, *.css or any file you want :-)

enjoy!
http://xdaks.deviantart.com
