#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'gui' (Qt4 based Main Window and GUI Core).
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import sys,io
from PyQt4 import Qt,QtCore,QtGui

class module(object):
	"""Main Application Window for QT UI."""
	def __init__(self, **params):
		"""
		Creates QT GUI MainWindow.
		Parameters:
			iCeDeROM object reference (mandatory).
			argv     from sys.argv (mandatory).
		"""
		self.app=QtGui.QApplication(params['argv'])
		self.name='gui'
		self.docks=dict()
		self.tabs=dict()
		self.texts=dict()
		self.createMainWindow(**params)
		self.createDocks(**params)

	def start(self, **params):
		self.window.show()
		return self.app.exec_()

	def stop(self, **params):
		self.logfp.close()
		self.app.quit()

	def setup(self, **params):
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		self.setupMainWindow(**params)
		self.setupDocks(**params)

	def createMainWindow(self, **params):
		#MainWindow and MdiArea
		self.window=QtGui.QMainWindow()		
		self.mdi=QtGui.QMdiArea()

	def setupMainWindow(self, **params):
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		self.window.setCentralWidget(self.mdi)
		self.window.setWindowTitle('iCeDeROM ('+params['iCeDeROM'].release+')')
		self.mdi.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.mdi.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.window.showMaximized()
		self.window.raise_()

	def createDocks(self, **params):
		#Information Dock and its contents
		self.texts['log']=QtGui.QTextEdit()
		self.texts['log'].setAcceptRichText(False)
		self.texts['log'].setReadOnly(True)
		self.texts['log'].setFontFamily("Courier")
		self.tabs['info']=QtGui.QTabWidget()
		self.tabs['info'].addTab(self.texts['log'], 'log')
		self.docks['info']=QtGui.QDockWidget()
		self.docks['info'].setWindowTitle('info')
		self.docks['info'].setMinimumSize(250,50)
		self.docks['info'].setFeatures(
			QtGui.QDockWidget.DockWidgetVerticalTitleBar|
			QtGui.QDockWidget.AllDockWidgetFeatures)
		self.docks['info'].setWidget(self.tabs['info'])
		self.window.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.docks['info'])

	def setupDocks(self, **params):
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		self.logfswatcher=QtCore.QFileSystemWatcher([params['iCeDeROM'].modules['log'].filename])
		self.logfswatcher.connect(self.logfswatcher, QtCore.SIGNAL('fileChanged(QString)'),self.logFileWatcher)
		self.logfp=io.open(params['iCeDeROM'].modules['log'].filename,'rt')

	@QtCore.pyqtSlot(str)
	def logFileWatcher(self, path):
		self.texts['log'].insertPlainText(self.logfp.read())

