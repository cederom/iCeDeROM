#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'ftdi.uart_qt' (provides Qt GUI for ftdi.uart configuration).
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

from PyQt4 import QtCore,QtGui

class module(QtGui.QWidget):
	"""
	Provide Qt GUI for ftdi.uart configuration.
	"""
	def __init__(self, **params):
		"""Create QtWidget."""
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if params['iCeDeROM'].ui!='qt':
			raise Warning('Interface QtWidget requires Qt GUI running!')
		super(module, self).__init__()
		self.name='ftdi.uart_qt'
		self.buttons=dict()
		self.layouts=dict()
		self.trees=dict()
		self.cfg=dict()
		self.id=None
		self.createQtWidget(**params)

	def setup(self, **params):
		return

	def start(self, **params):
		if not params.has_key('iCeDeROM'):
			raise Warning('iCeDeROM parameter reference mandatory!')
		if params['iCeDeROM'].ui!='qt':
			raise Warning('Interface QtWidget requires Qt GUI running!')			
		#attach configuration widget
		self.id=params['iCeDeROM'].modules['interface'].ui['qt'].stacks['config'].addWidget(self)

	def stop(self, **params):
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if params['iCeDeROM'].ui!='qt':
			raise Warning('Interface QtWidget requires Qt GUI running!')	
		#detach configuration widget
		params['iCeDeROM'].modules['interface'].ui['qt'].stacks['config'].removeWidget(self)

	def createQtWidget(self, **params):
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if params['iCeDeROM'].ui!='qt':
			raise Warning('Interface QtWidget requires Qt GUI running!')
		self.layouts['config']=QtGui.QVBoxLayout(self)
		self.layouts['config'].setContentsMargins(5,5,5,5)		
		self.layouts['config'].setSpacing(0)
		self.trees['config']=QtGui.QTreeWidget(self)
		self.trees['config'].setSizePolicy(QtGui.QSizePolicy(
			QtGui.QSizePolicy.Minimum,
			QtGui.QSizePolicy.Maximum))
		self.layouts['config'].addWidget(self.trees['config'])
		self.buttons['apply']=QtGui.QPushButton('Apply Configuration')
		self.layouts['config'].addWidget(self.buttons['apply'])
		#Fill in the information into the TreeWidget
		self.trees['config'].setHeaderItem(QtGui.QTreeWidgetItem(['parameter','value','descrption']))
		self.cfg['device']=QtGui.QTreeWidgetItem(self.trees['config'], ['Device'])
		self.cfg['vidpid']=QtGui.QTreeWidgetItem(self.cfg['device'],['VID/PID', '0xBBE2:0xABCD','USB VID/PID of the interface device.'])
		self.cfg['serial']=QtGui.QTreeWidgetItem(self.cfg['device'], ['serial', '', 'Serial number of the same VID/PID interface if you have more than one connected.'])
		self.cfg['index']=QtGui.QTreeWidgetItem(self.cfg['device'],['index','0','Index of the device with the same VID/PID interface if you have more than one connected.'])
		self.cfg['uart']=QtGui.QTreeWidgetItem(self.trees['config'], ['UART'])
		self.cfg['baudrate']=QtGui.QTreeWidgetItem(self.cfg['uart'],['baudrate','115200','Transmission speed in bits-per-second.'])
		self.cfg['mode']=QtGui.QTreeWidgetItem(self.cfg['uart'],['mode', 'B', 'Select connection mode: \'T\'ext or \'B\'inary (default).'])
		self.cfg['encoding']=QtGui.QTreeWidgetItem(self.cfg['uart'], ['encoding', 'UTF-8', 'Default text encoding.'])

		

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

