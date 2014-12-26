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
		self.ui=dict()
		self.devcfg=dict()
		self.parent=None
		self.baudrates=[300,1200,2400,4800,9600,14400,19200,28800,38400,57600,115200,230400]
		#Try to run GUI if possible
		if params.has_key('iCeDeROM'):
			if params['iCeDeROM'].ui=='qt':
				params['parent']=self
				import uart_qt
				self.ui['qt']=uart_qt.module(**params)

	def setup(self, **params):
		"""Connect and/or Setup the pylibftdi device.
		Parameters:
			vid/pid   is the USB VID and/or PID number of your interface
			serial    is the serial number of the device
			mode      is the connect mode ('t'ext or 'b'inary, default 'b')
			encoding  is the encoding to use for operation (default latin1)	
			index     is the device index for equal VID/PID (default 0)
			interface is the device in case of multi-interface devices
			baudrate  is the transmission speed in bauds
		Returns:
			True      when successful
		Note: Some parameters are mandatory to connect to a physical device!
		"""
		cfg=dict()
		if params.has_key('vid'):
			if type(params['vid'])==type('a'):
				params['vid']=int(params['vid'],base=16)
				self.devcfg['vid']=params['vid']
			if pylibftdi.USB_VID_LIST.count(params['vid'])==0:
				pylibftdi.USB_VID_LIST.append(params['vid'])
		if params.has_key('pid'):
			if type(params['pid'])==type('a'):
				params['pid']=int(params['pid'],base=16)
				self.devcfg['pid']=params['pid']
			if pylibftdi.USB_PID_LIST.count(params['pid'])==0:
				pylibftdi.USB_PID_LIST.append(params['pid'])
		if params.has_key('serial'):
			if params['serial']!='':
				cfg['device_id']=params['serial']
		if params.has_key('channel'):
			cfg['interface_select']=params['channel']
		if params.has_key('mode'):
			mode=params['mode']
			if str(mode).lower()[0]=='t':
				cfg['mode']=params['mode']='t'
			else:
				cfg['mode']=params['mode']='b'
		if params.has_key('encoding'):
			cfg['encoding']=params['encoding']
		if params.has_key('index'):
			index=int(params['index'])
			if index>0:
				cfg['device_index']=index
		if params.has_key('interface'):
			cfg['interface_select']=int(params['interface'])
		#Connect to the device
		try:
			self.device=pylibftdi.Device(**cfg)
		except:
			if params.has_key('iCeDeROM'):
				params['iCeDeROM'].modules['log'].log.exception('FTDI UART Interface setup failed!')
				#TODO show message in error dialog
			return False
		if params.has_key('mode'):
			self.devcfg['mode']=params['mode']
		if params.has_key('baudrate'):
			self.devcfg['baudrate']=int(params['baudrate'])
			self.device.baudrate=self.devcfg['baudrate']
		if params.has_key('iCeDeROM'):
			params['iCeDeROM'].modules['log'].log.info('FTDI UART Interface connected: vid='+
				hex(self.devcfg['vid'])+' pid='+hex(self.devcfg['pid'])+' cfg='+str(cfg))
		
		#TODO remove the test comms
		for i in range(0,100):
			self.device.write('iCeDeROM TEST '+str(i)+'\r\n')
		return True

	def start(self, **params):
		if self.ui.has_key('qt'):
			self.ui['qt'].start(**params)

	def stop(self, **params):
		if self.ui.has_key('qt'):
			self.ui['qt'].stop(**params)

	def write(self, **params):
		self.device.write(data)

	def read(self, **params):
		return self.device.read()

