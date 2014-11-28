#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'QtMdiChildExample' (example of iCeDeROM Module with mdiChildWindow Qt GUI).
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import os
from PyQt4 import Qt,QtCore,QtGui,uic

uifilename='QtMdiChildExample.ui'

class module(object):
	"""Example Module with Qt mdiChild window."""
	def __init__(self, **params):
		"""
		Create Module and QtWidget.
		Parameters:
			iCeDeROM module reference (mandatory).
		"""		
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		self.name='QtMdiChildExampleModule'
		if params['iCeDeROM'].ui=='qt':
			self.window=QtWindow(**params)
	def setup(self,**params):
		self.window.setup(**params)
	def start(self, **params):
		self.window.start(**params)
	def stop(self, **params):
		self.window.stop(**params)


class QtWindow(QtGui.QMainWindow):
	"""Example Module, Qt mdiChildWindow."""
	def __init__(self, **params):
		"""
		Create window and add it to the iCeDeROM GUI.
		Parameters:
			iCeDeROM module reference (mandatory).
		"""
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		super(QtWindow, self).__init__()
		self.name='QtMdiChildExampleWindow'
		self.uifile=os.path.join(os.path.dirname(os.path.relpath(__file__)))+'/'+uifilename
		self.window=uic.loadUi(self.uifile, self)
		try:
			params['iCeDeROM'].modules['gui'].mdi.addSubWindow(self.window)
		except:
			params['iCeDeROM'].modules['log'].log.critical('Cannot addSubWindow!')
			raise
		self.window.setWindowTitle('QtMdiChildExample')
		self.window.connect(self.window.pushButton, QtCore.SIGNAL('clicked()'), lambda:self.listModules(**params))
	def setup(self, **params):
		return
	def start(self, **params):
		self.window.show()
	def stop(self, **params):
		elf.window.hide()

	def listModules(self, **params):
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		self.window.textBrowser.clear()
		self.window.textBrowser.append('Available Modules:')
		for module in params['iCeDeROM'].modules:
			self.window.textBrowser.append(module)
