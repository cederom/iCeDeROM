#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'ui_qt_mdiChild_example' (example of module with mdiChildWindow GUI functionality).
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

from PyQt4 import Qt,QtCore,QtGui

class module(object):
	"""Simple example of Qt mdiChild window."""
	def __init__(self, **params):
		"""Creates window module and register to iCeDeROM modules."""
		self.name='ui_qt_mdiChild_example'
		self.mdiWindow=QtGui.QDialog()
		try:
			params['iCeDeROM'].modules['gui'].mdi.addSubWindow(self.mdiWindow)
		except:
			print 'You must provide a reference to iCeDeROM!'
	def setup(self, **params):
		self.mdiWindow.setWindowTitle('mdiChild example')
	def start(self, **params):
		self.mdiWindow.show()
	def stop(self, **params):
		elf.mdiWindow.hide()
