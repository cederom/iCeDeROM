#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'ftdi.uart' (provides UART comms with FTDI based interfaces).
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import pylibftdi

class module(object):
	"""
	Provides UART comms with FTDI based interfaces.
	"""
	def __init__(self, **params):
		"""Create FTDI UART Device.
		Note: Use Setup routine to connect to a physical Device.
		"""
		self.name='ftdi.uart'
		self.capabilities=['uart']
		self.isSetup=False

	def setup(self, **params):
		"""Connect and/or Setup the pylibftdi device.
		Parameters:
			vid/pid  is the USB VID and/or PID number of your interface
			mode     is the connect mode ('t'ext or 'b'inary, default 'b')
			serial   is the serial number of the device
			encoding is the encoding to use for operation (default latin1)	
			index    is the device index for equal VID/PID (default 0)
			baudrate is the transmission speed in bauds			
		Note: Some parameters are mandatory to connect to a physical device!
		"""
		if params.has_key('vid'):
			if pylibftdi.USB_VID_LIST.count(params['vid'])==0:
				pylibftdi.USB_VID_LIST.append(params['vid'])
			params.__delitem__('vid')
		if params.has_key('pid'):
			if pylibftdi.USB_PID_LIST.count(params['pid'])==0:
				pylibftdi.USB_PID_LIST.append(params['pid'])
			params.__delitem__('pid')
		self.device=pylibftdi.Device(**params)
		if params.has_key('mode'): self.device.mode=params['mode']
		if params.has_key('baudrate'): self.device.baudrate=params['baudrate']

	def start(self, **params):
		return

	def stop(self, **params):
		return

	def write(self, **params):
		self.device.write(data)

	def read(self, **params):
		return self.device.read()

