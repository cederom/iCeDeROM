#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'interface' (provides physical/electrical interface driver comms).
# (C) 2014-2015 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

devices = ['modules.interface.ftdi']

class module(object):
	"""
	Provides physical/electrical device driver comms.
	Various interface device modules can be loaded into the dictionary of devices.
	One of the device interfaces can be selected as default, 
	but others may still be used via self.devices dict() directly.
	"""
	def __init__(self, **params):
		"""
		Create iCeDeROM_Interface Module.
		Parameters:
			iCeDeROM is the reference to the iCeDeROM object.
		"""
		self.name='interface'
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		self.iCeDeROM=params['iCeDeROM']
		self.devices=dict()
		self.capabilities=list()
		self.device=None
		self.ui=dict()
		#Try to run GUI if possible
		if self.iCeDeROM.ui=='qt':
			import interface_qt
			self.ui['qt']=interface_qt.module(**params)

	def setup(self, **params):
		"""Setup the iCeDeROM_Interface Module."""
		self.loadAll(**params)
		self.list(**params)
		return
	
	def start(self, **params):
		"""Start the iCeDeROM_Interface Module."""
		if self.iCeDeROM.ui=='qt':
			self.ui['qt'].start(**params)
		return
	
	def stop(self, **params):
		"""Stop the iCeDeROM_Interface Module."""
		if self.iCeDeROM.ui=='qt':
			self.ui['qt'].stop(**params)		
		return

	def list(self, **params):
		"""
		Returns dictionary of loaded interface devices.
		This funcion will also log loaded interface devices
		and update the list inside UI if possible.
		"""
		self.iCeDeROM.modules['log'].log.info(
			'Loaded interface devices: '+str(self.devices.keys()))
		if self.ui.has_key('qt'):
			for dev in self.devices:
				self.ui['qt'].addDevice(name=dev)
		return self.devices
	
	def load(self, **params):
		"""Load interface device object to a list of available device drivers.
		Device object constructor is called here, but some devices may be
		attached to a physical interface at setup() or start() stage
		as additional configuration parameters may be obligatory to connect.
		If device was already loaded it will be replaced by new load.
		Params:
			name     is a driver module name (mandatory).
		"""
		try:
			params['iCeDeROM']=self.iCeDeROM
			self.devices[params['name']]=__import__(params['name'], fromlist=['']).module(**params)
			self.devices[params['name']].parent=self
			self.iCeDeROM.modules['log'].log.debug('Added '+params['name']+' interface device.')
			if self.ui.has_key('qt'):
				self.ui['qt'].stacks['config'].addWidget(
					self.devices[params['name']].ui['qt'])
		except:
			self.iCeDeROM.modules['log'].log.exception('Cannot add '+params['name']+' interface device!')

	def loadAll(self, **params):
		"""Load all interface devices according to module list defines."""
		for dev in devices:
			self.load(name=dev)
		
	def setDefault(self, **params):
		"""
		Select the default device for iCeDeROM_Interface Module.
		Device must be already loaded to devices dict with prior load() call.
		Parameters:
			name     is the name of interface to be selected as default.
		"""
		if not params.has_key('name'):
			self.iCeDeROM.modules['log'].error('name parameter reference mandatory!')
			raise KeyError('name parameter reference mandatory!')
		if self.devices.has_key(params['name']):
			self.device=self.devices[params['name']]
			self.iCeDeROM.modules['gui'].labels['interface'].setText(self.device.name)
			self.iCeDeROM.modules['log'].log.info('Selected '+params['name']+' as the default interface device.')
		else:
			self.iCeDeROM.modules['log'].log.warning('Interface device '+params['name']+' is not yet loaded!')

	def write(self, data):
		if self.device==None:
			raise IOError('Interface not yet initialized!')
		self.device.write(data)
			
	def read(self, length):
		if self.device==None:
			raise IOError('Interface not yet initialized!')
		return self.device.read(length)
