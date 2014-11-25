#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import sys
from icederom_ui_qt import *
from PyQt4 import Qt,QtGui

class MainWindow(object):
	def __init__(self):
		self.app=QtGui.QApplication(sys.argv)
		self.window=QtGui.QMainWindow()
		self.setup()
	def setup(self, **params):
		self.QtDesigner=Ui_MainWindow()
		self.QtDesigner.setupUi(self.window)
	def start(self, **params):
		self.window.showMaximized()
		self.window.raise_()
		self.window.show()
		sys.exit(self.app.exec_())
