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

class module(object):
	"""
	Provides interactive Python shell with Qt GUI capabilities.
	"""
	def __init__(self, **params):
		"""Creates logger."""
		self.name='python'
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		self.iCeDeROM=params['iCeDeROM']
		self.ui=dict()
		self.python=code.InteractiveConsole(params)
		#Create GUI part if possible
		if self.iCeDeROM.ui=='qt':
			import python_qt
			self.ui['qt']=python_qt.module(**params)
			code.sys.stdout=self.ui['qt']
			self.ui['qt'].execute=self.python.push
			self.python.write=self.ui['qt'].write
			self.ui['qt'].write('Python ('+code.sys.platform+') '+code.sys.version+'\n')

	def setup(self, **params):
		if self.iCeDeROM.ui=='qt':
			self.ui['qt'].setup(**params)
	
	def start(self, **params):
		if self.iCeDeROM.ui=='qt':
			self.ui['qt'].start(**params)

	def stop(self, **params):
		if self.iCeDeROM.ui=='qt':
			self.ui['qt'].stop(**params)

	def execute(self, command):
		self.python.resetbuffer()
		return self.python.push(command)
