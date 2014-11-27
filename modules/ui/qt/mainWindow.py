#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'gui' (Qt4 based Main Window and GUI Core).
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import sys
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
		self.window=QtGui.QMainWindow()
		self.mdi=QtGui.QMdiArea()
		self.window.setCentralWidget(self.mdi)
	def setup(self, **params):
		try:
			self.window.setWindowTitle('iCeDeROM ('+params['iCeDeROM'].release+')')
		except:
			print 'You must provide a reference to iCeDeROM!'
			self.window.setWindowTitle('iCeDeROM (unknown)')
		self.mdi.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.mdi.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.window.showMaximized()
		self.window.raise_()
		self.window.show()
	def start(self, **params):
		sys.exit(self.app.exec_())
