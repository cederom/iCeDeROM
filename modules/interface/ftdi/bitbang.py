#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'ftdi.bitbang' (provides BITBANG comms with FTDI based interfaces).
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import pylibftdi

class module(object):
	"""
	Provides BITBANG comms with FTDI based interfaces.
	"""
	def __init__(self, **params):
		"""Creates logger."""
		self.name='ftdi.bitbang'
		self.capabilities=['bitbang']
		self.device=pylibftdi.Device()

	def setup(self, **params):
		"""Setup the pylibftdi device.
			Parameters:
				mode     is the access mode type (default='t')
				baudrate is the transmission speed in bauds
		"""
		return
	
	def start(self, **params):
		return

	def stop(self, **params):
		return

	def write(self, **params):
		self.device.direction=dir
		self.device.port=data

	def read(self, **params):
		return self.device.port
