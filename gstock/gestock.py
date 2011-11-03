#!/usr/bin/env python
# encoding=utf-8

import time
from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import QUrl, SIGNAL, SLOT
from PyQt4.QtGui import QApplication, QMainWindow, QAction, QMenuBar

APP_URL = 'http://127.0.0.1:8094/'
        
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.menubar = QMenuBar()
        file_ = self.menubar.addMenu(u"&Fichier")
        exit = QAction(u"Quitter", self)
        exit.setShortcut("Ctrl+Q")
        exit.setToolTip("Quitter l'application")
        self.menubar.connect(exit, SIGNAL("triggered()"), \
                                         self, \
                                         SLOT("close()"))

        file_.addAction(exit)
        self.setMenuBar(self.menubar)
        self.web = QWebView()
        self.web.load(QUrl(APP_URL))
        self.setCentralWidget(self.web)
    
    def goto(self, url):
        self.web.load(QUrl(url))
    
    
def django_alive():
    import urllib2
    try:
        resp = urllib2.urlopen(APP_URL)
    except:
        return False
    return True

if __name__ == '__main__':
    import sys
    import os
    import subprocess
    import signal
    
    if not django_alive():
        p = subprocess.Popen("./manage.py runserver 0.0.0.0:8094", shell=True)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    time.sleep(3)
    window.showMaximized()
    sys.exit(app.exec_())
