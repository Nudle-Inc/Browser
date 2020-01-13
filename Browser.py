#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 22:38:58 2019

@author: jonathanziebarth - Edit of Browser on Github 
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

import os
import sys


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("The Ghost Browser")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)


        layout.addWidget(QLabel("Version 1.0"))
        layout.addWidget(QLabel("Copyright 2019 Nudle Inc."))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
#_____________________________________________________________________________
        #MAIN WINDOW

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(17, 17))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('Backward.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('Forward.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)


        reload_btn = QAction(QIcon(os.path.join('Refresh.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('Home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()  # Yes, really!
        self.httpsicon.setPixmap(QPixmap(os.path.join('lock.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
        
        
    
       
#________________________________________________________________________________
        # Uncomment to disable native menubar on Mac
        #self.menuBar().setNativeMenuBar(False)

#FILE MENU

        file_menu = self.menuBar().addMenu("&File")

        new_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)
        
        new_window_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "New Window", self)
        new_window_action.setStatusTip("Open a new window")
        new_window_action.triggered.connect(lambda _: self.add_new_window())
        file_menu.addAction(new_window_action)
        
        last_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "Reopen Last Tab", self)
        last_tab_action.setStatusTip("Open a new window")
        last_tab_action.triggered.connect(lambda _: self.open_last_tab())
        file_menu.addAction(last_tab_action)
        
        open_file_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "Open File...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(lambda _: self.open_file())
        file_menu.addAction(open_file_action )
        
        close_window_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "Close Window", self)
        close_window_action.setStatusTip("Close window")
        close_window_action.triggered.connect(lambda _: self.close_window())
        file_menu.addAction(close_window_action)
        
        close_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "Close Tab", self)
        close_tab_action.setStatusTip("Close tab")
        close_tab_action.triggered.connect(lambda _: self.close_current_tab())
        file_menu.addAction(close_tab_action)
        
        save_page_as_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "Save Page As", self)
        save_page_as_action.setStatusTip("Save Page As")
        save_page_as_action.triggered.connect(lambda _: self.save_page_as())
        file_menu.addAction(save_page_as_action)
        
        print_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "Print...", self)
        print_action.setStatusTip("Print")
        print_action.triggered.connect(lambda _: self.print())
        file_menu.addAction(print_action)
#_____________________________________________________________
        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Undo Do", self)
        undo_action.setStatusTip("Go to nudle.com")
        undo_action.triggered.connect(self.undo_typing)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Redo", self)
        redo_action.setStatusTip("Go to nudle.com")
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        cut_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Cut", self)
        cut_action.setStatusTip("Go to nudle.com")
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"copy", self)
        copy_action.setStatusTip("Go to nudle.com")
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        paste_action.setStatusTip("Go to nudle.com")
        paste_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(paste_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
  #_____________________________________________________________ 
        view_menu = self.menuBar().addMenu("&View")

        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        view_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
  #_____________________________________________________________ 
        history_menu = self.menuBar().addMenu("&History")

        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        history_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        edit_menu.addAction(navigate_nudle_action)
        
        #Recently Closed 
        
        #history 
        
  #_____________________________________________________________ 
        bookmark_menu = self.menuBar().addMenu("&Bookmarks")

        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        bookmark_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        bookmark_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        bookmark_menu.addAction(navigate_nudle_action)
  #______________________________________________________ 
        profile_menu = self.menuBar().addMenu("&Profiles")

        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        profile_menu.addAction(navigate_nudle_action)
    #______________________________________________________ 
        tab_menu = self.menuBar().addMenu("&Tab")

        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        tab_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        bookmark_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        bookmark_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        bookmark_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        bookmark_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        bookmark_menu.addAction(navigate_nudle_action)
  #_____________________________________________________________    
        window_menu = self.menuBar().addMenu("&Window")

        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        window_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        window_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        window_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        window_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        window_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        window_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        window_menu.addAction(navigate_nudle_action)
        
        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        window_menu.addAction(navigate_nudle_action)
  #_____________________________________________________________    
        help_menu = self.menuBar().addMenu("&Help")

        navigate_nudle_action = QAction(QIcon(os.path.join('images', 'Forward.png')),"Nudle", self)
        navigate_nudle_action.setStatusTip("Go to nudle.com")
        navigate_nudle_action.triggered.connect(self.navigate_nudle)
        help_menu.addAction(navigate_nudle_action)
        
        
  #_____________________________________________________________    

        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        self.show()

#_______________________
        
    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl('http://www.google.com')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        # More difficult! We only want to update the url when it's from the
        # correct tab
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()
    
    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()      
        

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)
#_______________________________________________________________________________
    def navigate_nudle(self):
        self.tabs.currentWidget().setUrl(QUrl("https://nudleinc.xyz"))

#_______________________

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):  # Does not receive the Url
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)
#____________________
    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        if q.scheme() == 'https':
            # Secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('lock.png')))

        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('stop.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
#_______________________
    def show_history_action(self):
        self.tab_open_doubleclick(QWebEngineHistory)
#_______________________
       
        
app = QApplication(sys.argv)
app.setApplicationName("Ghost")
app.setOrganizationName("Nudle")
app.setOrganizationDomain("Nudleinc.xyz")

window = MainWindow()

app.exec_()
