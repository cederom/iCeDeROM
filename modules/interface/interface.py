#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'interface' (provides physical/electrical interface driver comms).
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

devices = ['modules.interface.ftdi.uart'] #'modules.interface.ftdi.bitbang']

class module(object):
	"""
	Provides physical/electrical device driver comms.
	Various interface device modules can be loaded into the dictionary of devices.
	One of the device interfaces can be selected as default, 
	but others may still be used via self.devices dict() directly.
	"""
	def __init__(self, **params):
		"""
		Creates iCeDeROM_Interface Module.
		Parameters:
			iCeDeROM is the reference to the iCeDeROM object.
		"""
		self.name='interface'
		self.devices=dict()
		self.capabilities=list()
		self.device=None
		#Try to run GUI if possible
		if params.has_key('iCeDeROM'):
			if params['iCeDeROM'].ui=='qt':
				import interface_qt
				self.window=interface_qt.module(**params)

	def setup(self, **params):
		"""Setup the iCeDeROM_Interface Module."""
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		self.loadAll(**params)
		self.list(**params)
		return
	
	def start(self, **params):
		"""Start the iCeDeROM_Interface Module."""
		if params.has_key('iCeDeROM'):
			if params['iCeDeROM'].ui=='qt':	
				self.window.start(**params)
		return
	
	def stop(self, **params):
		"""Stop the iCeDeROM_Interface Module."""
		if params.has_key('iCeDeROM'):
			if params['iCeDeROM'].ui=='qt':
				self.window.stop(**params)		
		return

	def list(self, **params):
		"""
		Returns dictionary of loaded interface devices.
		This funcion will also log loaded interface devices
		and update the list inside QtWidget if possible.
		Parameters:
			iCeDeROM is the reference to the iCeDeROM object (optional).
		"""
		if params.has_key('iCeDeROM'):
			params['iCeDeROM'].modules['log'].log.info(
				'Loaded interface devices: '+str(self.devices.keys()))
			if params['iCeDeROM'].ui=='qt':
				for dev in self.devices:
					self.window.addDevice(iCeDeROM=params['iCeDeROM'], name=dev)
		return self.devices
	
	def load(self, **params):
		"""Load interface device object to a list of available device drivers.
		Device object constructor is called here, but some devices may be
		attached to a physical interface at setup() or start() stage
		as additional configuration parameters may be obligatory to connect.
		Params:
			iCeDeROM (manatory)
			name     is a driver module name (mandatory).
		"""
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		try:
			if not self.devices.has_key(params['name']):
				self.devices[params['name']]=__import__(params['name'], fromlist=['']).module()
				params['iCeDeROM'].modules['log'].log.debug('Added '+params['name']+' interface device.')
				return True
		except:
			params['iCeDeROM'].modules['log'].log.exception('Cannot add '+params['name']+' interface device!')
			return False

	def loadAll(self, **params):
		"""Load all interface devices according to module list defines."""
		for dev in devices:
			self.load(iCeDeROM=params['iCeDeROM'], name=dev)
		
	def setDefault(self, **params):
		"""
		Select the default device for iCeDeROM_Interface Module.
		Device must be already loaded to devices dict with prior load() call.
		Parameters:
			iCeDeROM is the reference to the iCeDeROM object.
			name     is the name of interface to be selected as default.
		"""
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if not params.has_key('name'):
			params['iCeDeROM'].modules['log'].error('name parameter reference mandatory!')
			raise KeyError('name parameter reference mandatory!')
		if self.devices.has_key(params['name']):
			self.device=self.devices[params['name']]
			params['iCeDeROM'].modules['log'].log.info('Selected '+params['name']+' as the default interface device.')
		else:
			params['iCeDeROM'].modules['log'].log.warning('Interface device '+params['name']+' is not yet loaded!')
