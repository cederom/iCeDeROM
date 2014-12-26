#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'drv_qt' (provides Qt GUI for iCeDeROM_Driver).
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

from PyQt4 import QtCore,QtGui

class module(QtGui.QWidget):
	"""
	Provides basic Qt GUI for iCeDeROM_Driver.
	"""
	def __init__(self, **params):
		"""Creates QtWidget."""
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if params['iCeDeROM'].ui!='qt':
			raise Warning('Interface QtWidget requires Qt GUI running!')
		super(module, self).__init__()	
		self.name='interface_qt'
		self.lists=dict()
		self.buttons=dict()
		self.layouts=dict()
		self.groups=dict()
		self.stacks=dict()
		self.id=None
		self.createQtWidget(**params)
		self.device=None

	def setup(self, **params):
		return

	def start(self, **params):
		if not params.has_key('iCeDeROM'):
			raise Warning('iCeDeROM parameter reference mandatory!')
		if params['iCeDeROM'].ui!='qt':
			raise Warning('Interface QtWidget requires Qt GUI running!')			
		params['iCeDeROM'].modules['gui'].tabs['info'].setUpdatesEnabled(False)
		self.id=params['iCeDeROM'].modules['gui'].tabs['info'].addTab(self, 'interface')
		params['iCeDeROM'].modules['gui'].tabs['info'].setUpdatesEnabled(True)

	def stop(self, **params):
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if params['iCeDeROM'].ui!='qt':
			raise Warning('Interface QtWidget requires Qt GUI running!')	
		params['iCeDeROM'].modules['gui'].tabs['info'].setUpdatesEnabled(False)
		params['iCeDeROM'].modules['gui'].tabs['info'].delTab(self.id)
		params['iCeDeROM'].modules['gui'].tabs['info'].setUpdatesEnabled(True)

	def createQtWidget(self, **params):
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if params['iCeDeROM'].ui!='qt':
			raise Warning('Interface QtWidget requires Qt GUI running!')			
		self.layouts['interface']=QtGui.QHBoxLayout(self)
		self.groups['device']=QtGui.QGroupBox('Device')
		self.groups['device'].setFixedWidth(250)
		self.layouts['interface'].addWidget(self.groups['device'])
		self.layouts['device']=QtGui.QVBoxLayout(self.groups['device'])
		self.lists['device']=QtGui.QListWidget()
		self.buttons['default']=QtGui.QPushButton('Set Defatult Interface')
		self.connect(self.buttons['default'],
			QtCore.SIGNAL('clicked()'), lambda:self.test(**params))
		self.layouts['device'].addWidget(self.lists['device'])
		self.layouts['device'].addWidget(self.buttons['default'])
		self.groups['config']=QtGui.QGroupBox('Configuration')
		self.layouts['interface'].addWidget(self.groups['config'])
		self.layouts['config']=QtGui.QHBoxLayout(self.groups['config'])
		self.stacks['config']=QtGui.QStackedWidget()
		self.layouts['config'].addWidget(self.stacks['config'])
		self.layouts['config'].setContentsMargins(0,0,0,0)

	def addDevice(self, **params):
		"""
		Add Device Module to the devices list.
		Parameters:
			iCeDeROM  is the reference to the iCeDeROM object.
			name      is the name of interface module to add.
		"""
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if not params.has_key('name'):
			raise KeyError('name parameter reference mandatory!')
		if params['iCeDeROM'].ui!='qt':
			raise Warning('Interface QtWidget requires Qt GUI running!')
		self.lists['device'].addItem(params['name'])

	def select(self, **params):
		"""
		Handle Qt GUI the selection from the interface device list.
		Device interface configuration is displayed.
		Parameters:
			iCeDeROM is the reference to the iCeDeROM object.
			name     is the interface name to be selected.
		"""
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if not params.has_key('name'):
			raise KeyError('name parameter reference mandatory!')		
		if params['iCeDeROM'].modules['interface'].devices.has_key(params['name']):
			if self.device!=None:
				self.device.stop()
			self.device=params['iCeDeROM'].modules['interface'].devices[params['name']]
			self.device.start(**params)
		else:
			params['iCeDeROM'].modules['log'].log.warning(
				'Device interface '+params['name']+' is not (yet) loaded!')

	def test(self,**params):
		params['iCeDeROM'].modules['interface'].devices['modules.interface.ftdi.uart'].write('iCeDeROM TEST...\n')

			