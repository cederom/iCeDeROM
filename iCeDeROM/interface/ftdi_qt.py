#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'ftdi.uart_qt' (provides Qt GUI for ftdi.uart configuration).
# (C) 2014-2017 CeDeROM Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

from PyQt4 import QtCore, QtGui
import ftdi


class module(QtGui.QWidget):
    """
	Provide Qt GUI for ftdi.uart configuration.
	"""

    def __init__(self, **params):
        """Create QtWidget."""
        self.name = 'ftdi.uart_qt'
        if not 'iCeDeROM' in params:
            raise KeyError('iCeDeROM parameter reference mandatory!')
        if params['iCeDeROM'].ui != 'qt':
            raise RuntimeError('Interface QtWidget requires Qt GUI running!')
        self.iCeDeROM = params['iCeDeROM']
        super(module, self).__init__()
        self.buttons = dict()
        self.layouts = dict()
        self.trees = dict()
        self.id = None
        self.defaults = dict()
        self.defaults['baudrate'] = '115200'
        self.defaults['interface'] = 'KT-LINK'
        self.devcfg = dict()
        self.parent = None
        if 'parent' in params: self.parent = params['parent']
        self.createQtWidget(**params)

    def setup(self, **params):
        '''Setup the QtWidget components, add fields and values, etc.'''
        return

    def start(self, **params):
        '''Start the QtWidget and attach it to Device Interface Configuration stack widget.'''
        if self.iCeDeROM.ui != 'qt':
            raise RuntimeError('Interface QtWidget requires Qt GUI running!')
        # attach configuration widget
        self.id = self.iCeDeROM.modules['interface'].ui['qt'].stacks['config'].addWidget(self)

    def stop(self, **params):
        '''Stop the QtWidget and detach it from the Device Interface Configuration stack widget.'''
        if self.iCeDeROM.ui != 'qt':
            raise RuntimeError('Interface QtWidget requires Qt GUI running!')
        # detach configuration widget
        self.iCeDeROM.modules['interface'].ui['qt'].stacks['config'].removeWidget(self)

    def createQtWidget(self, **params):
        '''Create the QtWidget elements.'''
        if self.iCeDeROM.ui != 'qt':
            raise Warning('Interface QtWidget requires Qt GUI running!')
        self.layouts['config'] = QtGui.QVBoxLayout(self)
        self.layouts['config'].setContentsMargins(5, 5, 5, 5)
        self.layouts['config'].setSpacing(0)
        self.trees['config'] = QtGui.QTreeWidget(self)
        self.trees['config'].setMinimumHeight(100)
        self.trees['config'].setSizePolicy(QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Minimum))
        self.layouts['config'].addWidget(self.trees['config'])
        self.buttons['apply'] = QtGui.QPushButton('Apply Configuration')
        self.layouts['config'].addWidget(self.buttons['apply'])
        self.connect(self.buttons['apply'],
                     QtCore.SIGNAL('clicked()'), lambda: self.configApply(**params))
        # Populate the TreeWidget
        self.trees['config'].setHeaderItem(QtGui.QTreeWidgetItem(['parameter', 'value', 'descrption']))
        self.trees['config'].setColumnWidth(1, 150)
        # DEVICE branch
        self.trees['device'] = QtGui.QTreeWidgetItem(self.trees['config'], ['Device'])
        # Interface
        self.trees['interface'] = QtGui.QTreeWidgetItem(self.trees['device'],
                                                        ['Interface', 'hardware', 'Interface Device Configuration.'])
        self.buttons['interface'] = QtGui.QComboBox()
        self.trees['config'].setItemWidget(self.trees['interface'], 1, self.buttons['interface'])
        # VID
        self.trees['vid'] = QtGui.QTreeWidgetItem(self.trees['device'],
                                                  ['VID', '0xCDCD', 'USB VID of the interface device.'])
        self.buttons['vid'] = QtGui.QLineEdit()
        self.buttons['vid'].setReadOnly(False)
        self.trees['config'].setItemWidget(self.trees['vid'], 1, self.buttons['vid'])
        # PID
        self.trees['pid'] = QtGui.QTreeWidgetItem(self.trees['device'],
                                                  ['PID', '0xBEEF', 'USB PID of the interface device.'])
        self.buttons['pid'] = QtGui.QLineEdit()
        self.buttons['pid'].setReadOnly(False)
        self.trees['config'].setItemWidget(self.trees['pid'], 1, self.buttons['pid'])
        # Fill in the Interface selection list
        for interface in ftdi.interfaces:
            self.buttons['interface'].insertItem(0, interface)
        if self.defaults['interface'] != None:
            i = self.buttons['interface'].findText(self.defaults['interface'])
            if i >= 0: self.buttons['interface'].setCurrentIndex(i)
        # Serial
        self.trees['serial'] = QtGui.QTreeWidgetItem(self.trees['device'],
                                                     ['serial', '',
                                                      'Serial number of the same VID/PID interface if you have more than one connected.'])
        self.buttons['serial'] = QtGui.QLineEdit()
        self.trees['config'].setItemWidget(self.trees['serial'], 1, self.buttons['serial'])
        # Index
        self.trees['index'] = QtGui.QTreeWidgetItem(self.trees['device'],
                                                    ['index', '0',
                                                     'Index of the device with the same VID/PID interface if you have more than one connected.'])
        self.buttons['index'] = QtGui.QSpinBox()
        self.trees['config'].setItemWidget(self.trees['index'], 1, self.buttons['index'])
        # UART branch
        self.trees['uart'] = QtGui.QTreeWidgetItem(self.trees['config'], ['UART'])
        # Interface
        self.trees['channel'] = QtGui.QTreeWidgetItem(self.trees['uart'], ['Channel'])
        self.buttons['channel'] = QtGui.QComboBox()
        self.buttons['channel'].setEditable(True)
        self.trees['config'].setItemWidget(self.trees['channel'], 1, self.buttons['channel'])
        # Baudrate
        self.trees['baudrate'] = QtGui.QTreeWidgetItem(self.trees['uart'],
                                                       ['baudrate', '115200', 'Transmission speed in bits-per-second.'])
        self.buttons['baudrate'] = QtGui.QComboBox()
        self.buttons['baudrate'].setEditable(True)
        for rate in self.parent.baudrates:
            self.buttons['baudrate'].addItem(str(rate))
        self.buttons['baudrate'].setCurrentIndex(self.buttons['baudrate'].findText(self.defaults['baudrate']))
        self.trees['config'].setItemWidget(self.trees['baudrate'], 1, self.buttons['baudrate'])
        # Mode
        self.trees['mode'] = QtGui.QTreeWidgetItem(self.trees['uart'],
                                                   ['mode', 'B',
                                                    'Select connection mode: \'T\'ext or \'B\'inary (default).'])
        self.buttons['mode'] = QtGui.QComboBox()
        self.buttons['mode'].addItem('T')
        self.buttons['mode'].addItem('B')
        self.trees['config'].setItemWidget(self.trees['mode'], 1, self.buttons['mode'])
        # Encoding
        self.trees['encoding'] = QtGui.QTreeWidgetItem(self.trees['uart'],
                                                       ['encoding', 'UTF-8', 'Default text encoding.'])
        self.buttons['encoding'] = QtGui.QComboBox()
        self.buttons['encoding'].setEditable(True)
        self.buttons['encoding'].addItem('latin1')
        self.buttons['encoding'].addItem('latin2')
        self.trees['config'].setItemWidget(self.trees['encoding'], 1, self.buttons['encoding'])
        # Connect signals
        self.connect(self.buttons['interface'],
                     QtCore.SIGNAL('activated(int)'), self.updateInterfaceParameters)
        # Update default confguration parameters
        self.updateInterfaceParameters(**params)

    def addDevice(self, **params):
        """
		Add Device Module to the devices list.
		Parameters:
			name      is the name of interface module to add.
		"""
        if not 'name' in params:
            raise KeyError('name parameter reference mandatory!')
        if self.iCeDeROM.ui != 'qt':
            raise RuntimeError('Interface QtWidget requires Qt GUI running!')
        self.lists['device'].addItem(params['name'])

    def updateInterfaceParameters(self, **params):
        '''Update the configuration widget values when interface is selected.'''
        ifname = str(self.buttons['interface'].currentText().toAscii())
        if ifname == 'Custom':
            self.buttons['vid'].setReadOnly(False)
            self.buttons['pid'].setReadOnly(False)
            self.buttons['channel'].setEditable(True)
        else:
            self.buttons['vid'].setReadOnly(True)
            self.buttons['pid'].setReadOnly(True)
            self.buttons['channel'].setEditable(False)
        self.buttons['vid'].setText(hex(ftdi.interfaces[ifname]['vid']))
        self.buttons['pid'].setText(hex(ftdi.interfaces[ifname]['pid']))
        self.buttons['channel'].insertItem(0, str(ftdi.interfaces[ifname]['uart_interface']))
        self.buttons['channel'].setCurrentIndex(0)

    def configRead(self, **params):
        '''Read widget values into variables and return as dictionary.'''
        try:
            self.devcfg['vid'] = str(self.buttons['vid'].text())
            self.devcfg['pid'] = str(self.buttons['pid'].text())
            self.devcfg['mode'] = str(self.buttons['mode'].currentText().toAscii().toLower())
            self.devcfg['serial'] = str(self.buttons['serial'].text())
            self.devcfg['encoding'] = str(self.buttons['encoding'].currentText().toAscii())
            self.devcfg['index'] = self.buttons['index'].value()
            self.devcfg['baudrate'] = int(self.buttons['baudrate'].currentText().toAscii())
            self.devcfg['channel'] = int(self.buttons['channel'].currentText().toAscii())
        except:
            self.iCeDeROM.modules['log'].log.exception('Configuration read failed!')
            return False
        return self.devcfg

    def configApply(self, **params):
        '''Apply provided configuration on an Interface Device.'''
        self.configRead()
        params.update(self.devcfg)
        self.parent.setup(**params)
