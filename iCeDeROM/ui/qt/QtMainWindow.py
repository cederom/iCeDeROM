#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'gui' (Qt4 based Main Window and GUI Core).
# (C) 2014-2017 CeDeROM Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import sys, io
from PyQt5 import Qt, QtCore, QtWidgets


class module(object):
    """Main Application Window for QT UI."""

    def __init__(self, **params):
        """
        Creates QT GUI MainWindow.
        Parameters:
            iCeDeROM object reference (mandatory).
            argv     from sys.argv (mandatory).
        You can override QtStyle with '-style' commandline option.
        """
        self.name = 'gui'
        self.description = 'PyQt5'
        if not 'iCeDeROM' in params:
            raise KeyError('iCeDeROM parameter reference mandatory!')
        self.iCeDeROM = params['iCeDeROM']
        QtWidgets.QApplication.setStyle('cleanlooks')
        self.app = QtWidgets.QApplication(params['argv'])
        self.docks = dict()
        self.tabs = dict()
        self.dialogs = dict()
        self.labels = dict()
        self.menu = None
        self.menus = dict()
        self.createMainWindow(**params)
        self.createMenus(**params)
        self.createDocks(**params)
        self.createDialogs(**params)

    def start(self, **params):
        self.window.show()
        return self.app.exec_()

    def stop(self, **params):
        self.app.quit()

    def setup(self, **params):
        self.setupMainWindow(**params)
        self.setupMenus(**params)
        self.setupDocks(**params)

    def createMainWindow(self, **params):
        self.window = QtWidgets.QMainWindow()
        self.mdi = QtWidgets.QMdiArea(self.window)
        self.statusbar = QtWidgets.QStatusBar(self.window)
        self.labels['filenameL'] = QtWidgets.QLabel(self.window)
        self.labels['filename'] = QtWidgets.QLabel(self.window)
        self.labels['interfaceL'] = QtWidgets.QLabel(self.window)
        self.labels['interface'] = QtWidgets.QLabel(self.window)
        self.labels['progress'] = QtWidgets.QProgressBar(self.window)

    def setupMainWindow(self, **params):
        # Main Window
        self.window.setCentralWidget(self.mdi)
        self.window.setWindowTitle('iCeDeROM (' + params['iCeDeROM'].release + ')')
        # MDI
        self.mdi.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdi.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        # Status Bar
        self.window.setStatusBar(self.statusbar)
        self.labels['filenameL'].setText('F:')
        # TODO make filename label elice/truncate long strings and not impact window size
        self.labels['filename'].setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken)
        self.labels['filename'].setText('None')
        self.labels['interfaceL'].setText('IF:')
        self.labels['interface'].setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken)
        self.labels['interface'].setWordWrap(False)
        self.labels['interface'].setText('None')
        self.labels['progress'].setTextVisible(False)
        self.statusbar.addWidget(self.labels['filenameL'])
        self.statusbar.addWidget(self.labels['filename'], 10)
        self.statusbar.addWidget(self.labels['interfaceL'])
        self.statusbar.addWidget(self.labels['interface'])
        self.statusbar.addPermanentWidget(self.labels['progress'])
        self.window.showMaximized()
        self.window.raise_()

    def createDocks(self, **params):
        # System Dock and its contents
        self.tabs['system'] = QtWidgets.QTabWidget()
        self.docks['system'] = QtWidgets.QDockWidget()
        self.docks['system'].setWindowTitle('System')
        self.docks['system'].setMinimumSize(250, 50)
        self.docks['system'].setFeatures(
            QtWidgets.QDockWidget.DockWidgetVerticalTitleBar |
            QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.docks['system'].setWidget(self.tabs['system'])
        self.window.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.docks['system'])
        self.tabs['system'].addTab(
            self.iCeDeROM.modules['log'].createQtWidget(**params),
            self.iCeDeROM.modules['log'].name)

    def setupDocks(self, **params):
        return

    def createDialogs(self, **params):
        self.dialogs['message'] = QtWidgets.QMessageBox(self.window)
        self.dialogs['file'] = QtWidgets.QFileDialog(self.window)

    def createMenus(self, **params):
        self.menu = self.window.menuBar()

    def setupMenus(self, **params):
        self.menus['window'] = self.menu.addMenu('Window')
        self.menus['arrange'] = self.menus['window'].addMenu('Arrange')
        self.menus['arrange'].addAction('Tabs', self.setMdiTabbed)
        self.menus['arrange'].addAction('Windows', self.setMdiWindowed)
        self.menus['arrange'].addSeparator()
        self.menus['arrange'].addAction('Cascade Windows', self.setMdiCascaded)
        self.menus['arrange'].addAction('Tile Windows', self.setMdiTiled)
        self.menus['modules'] = self.menu.addMenu('Modules')
        self.menus['help'] = self.menu.addMenu('Help')
        self.menus['help'].addAction('About iCeDeROM', lambda: self.aboutApplication(**params))
        self.menus['help'].addAction('About Qt', self.aboutQt)

    def setMdiTabbed(self):
        self.mdi.setViewMode(QtWidgets.QMdiArea.TabbedView)

    def setMdiWindowed(self):
        self.mdi.setViewMode(QtWidgets.QMdiArea.SubWindowView)

    def setMdiCascaded(self):
        self.mdi.cascadeSubWindows()

    def setMdiTiled(self):
        self.mdi.tileSubWindows()

    def aboutApplication(self, **params):
        version = '<br/>Version: <small>' + self.iCeDeROM.release + '</small>'
        self.dialogs['message'].about(self.window, 'About iCeDeROM',
                                      '<center>\
			<h1>iCeDeROM</h1>\
			<br/>In-Circuit Evaluate Debug and Edit for Research on Microelectronics\
			' + version + '\
			<br/><a href="http://www.icederom.com">http://www.icederom.com</a>\
			<br/><br/>(C) 2014-2015 Tomasz Boleslaw CEDRO\
			<br/><a href="http://www.tomek.cedro.info">http://www.tomek.cedro.info</a>\
			</center>')

    def aboutQt(self):
        self.dialogs['message'].aboutQt(self.window, 'About Qt')
