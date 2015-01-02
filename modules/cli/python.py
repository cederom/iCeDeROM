#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'python' (provides python shell and scripting with QT GUI capabilities).
# (C) 2014-2015 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)
#TODO: add file and script execution routine

import code
import python_qt

class module(object):
	"""
	Provides interactive Python shell with Qt GUI capabilities.
	"""
	def __init__(self, **params):
		"""Creates logger."""
		self.name='python'
		self.python=code.InteractiveConsole(params)
		#Create GUI part if necessary
		if not params.has_key('iCeDeROM'): return
		if not params['iCeDeROM'].modules.has_key('gui'): return
		self.pythonQt=python_qt.module(**params)
		code.sys.stdout=self.pythonQt
		self.pythonQt.execute=self.python.push
		self.python.write=self.pythonQt.write
		self.pythonQt.write('Python ('+code.sys.platform+') '+code.sys.version+'\n')

	def setup(self, **params):
		return
	
	def start(self, **params):
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if not params['iCeDeROM'].modules.has_key('gui'): return
		params['iCeDeROM'].modules['gui'].tabs['info'].setUpdatesEnabled(False)
		self.pythonQt.tabs[self.name]=params['iCeDeROM'].modules['gui'].tabs['info'].addTab(
			self.pythonQt, 'python')
		params['iCeDeROM'].modules['gui'].tabs['info'].setUpdatesEnabled(True)
		self.pythonQt.show()

	
	def stop(self, **params):
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if not params['iCeDeROM'].modules.has_key('gui'): return
		params['iCeDeROM'].modules['gui'].tabs['info'].setUpdatesEnabled(False)
		params['iCeDeROM'].modules['gui'].tabs['info'].removeTab(self.tabs[self.name])
		self.texts[self.name].hide()
		params['iCeDeROM'].modules['gui'].tabs['info'].setUpdatesEnabled(True)

	def execute(self, command):
		self.python.resetbuffer()
		return self.python.push(command)
