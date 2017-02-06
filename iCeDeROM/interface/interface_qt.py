#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'drv_qt' (provides Qt GUI for iCeDeROM_Driver).
# (C) 2014-2017 CeDeROM Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

from PyQt5 import QtCore, QtWidgets


class module(QtWidgets.QTabWidget):
    """
	Provides basic Qt GUI for iCeDeROM_Driver.
	"""

    def __init__(self, **params):
        """Creates QtWidget."""
        self.name = 'interface_qt'
        if not 'iCeDeROM' in params:
            raise KeyError('iCeDeROM parameter reference mandatory!')
        if params['iCeDeROM'].ui != 'qt':
            raise RuntimeError('Interface QtWidget requires Qt GUI running!')
        self.iCeDeROM = params['iCeDeROM']
        super(module, self).__init__()
        self.lists = dict()
        self.buttons = dict()
        self.layouts = dict()
        self.groups = dict()
        self.stacks = dict()
        self.id = None
        self.createQtWidget(**params)
        self.setupQtWidget(**params)
        self.device = None

    def setup(self, **params):
        return

    def start(self, **params):
        if self.iCeDeROM.ui != 'qt':
            raise RuntimeError('Interface QtWidget requires Qt GUI running!')
        self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(False)
        self.id = self.iCeDeROM.modules['gui'].tabs['system'].addTab(self, 'interface')
        self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(True)

    def stop(self, **params):
        if self.iCeDeROM.ui != 'qt':
            raise RuntimeError('Interface QtWidget requires Qt GUI running!')
        self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(False)
        self.iCeDeROM.modules['gui'].tabs['system'].delTab(self.id)
        self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(True)

    def createQtWidget(self, **params):
        self.layouts['interface'] = QtWidgets.QHBoxLayout(self)
        self.groups['device'] = QtWidgets.QGroupBox('Device')
        self.layouts['device'] = QtWidgets.QVBoxLayout(self.groups['device'])
        self.lists['device'] = QtWidgets.QListWidget()
        self.buttons['default'] = QtWidgets.QPushButton('Set Defatult Interface')
        self.groups['config'] = QtWidgets.QGroupBox('Configuration')
        self.layouts['config'] = QtWidgets.QHBoxLayout(self.groups['config'])
        self.stacks['config'] = QtWidgets.QStackedWidget()

    def setupQtWidget(self, **params):
        self.groups['device'].setFixedWidth(250)
        self.layouts['interface'].addWidget(self.groups['device'])
        # TODO: FIX SIGNALLING CODE
        # self.connect(self.buttons['default'],
        #	QtCore.SIGNAL('clicked()'), lambda:self.test(**params))
        self.layouts['device'].addWidget(self.lists['device'])
        self.layouts['device'].addWidget(self.buttons['default'])
        self.layouts['interface'].addWidget(self.groups['config'])
        self.layouts['config'].addWidget(self.stacks['config'])
        self.layouts['config'].setContentsMargins(0, 0, 0, 0)

    def addDevice(self, **params):
        """
		Add Device Module to the devices list.
		Parameters:
			name      is the name of interface module to add.
		"""
        if not params.has_key('name'):
            raise KeyError('name parameter reference mandatory!')
        if self.iCeDeROM.ui != 'qt':
            raise RuntimeError('Interface QtWidget requires Qt GUI running!')
        self.lists['device'].addItem(params['name'])

    def select(self, **params):
        """
		Handle Qt GUI the selection from the interface device list.
		Device interface configuration is displayed.
		Parameters:
			name     is the interface name to be selected.
		"""
        if not params.has_key('name'):
            raise KeyError('name parameter reference mandatory!')
        if self.iCeDeROM.modules['interface'].devices.has_key(params['name']):
            if self.device != None:
                self.device.stop()
            self.device = self.iCeDeROM.modules['interface'].devices[params['name']]
            self.device.start(**params)
        else:
            self.iCeDeROM.modules['log'].log.warning(
                'Device interface ' + params['name'] + ' is not (yet) loaded!')
