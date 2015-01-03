#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'Terminal' (terminal module for shell and/or serial port).
# (C) 2014-2015 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

class module(object):
	"""Example Module with Qt mdiChild window."""
	def __init__(self, **params):
		"""
		Create Module and QtWidget if necessary.
		Parameters:
			iCeDeROM module reference (mandatory).
		"""
		self.name='terminal'		
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		self.iCeDeROM=params['iCeDeROM']
		self.ui=dict()		
		if self.iCeDeROM.ui=='qt':
			import terminal_qt
			self.ui['qt']=terminal_qt.module(**params)
			self.ui['qt'].parent=self

	def setup(self,**params):
		if self.iCeDeROM.ui=='qt':
			self.ui['qt'].setup(**params)

	def start(self, **params):
		if self.iCeDeROM.ui=='qt':
			self.ui['qt'].start(**params)

	def stop(self, **params):
		if self.iCeDeROM.ui=='qt':
			self.ui['qt'].stop(**params)

	def write(self, data):
		self.iCeDeROM.modules['interface'].write(data)
		
	def read(self, length):
		return self.iCeDeROM.modules['interface'].read(length)
