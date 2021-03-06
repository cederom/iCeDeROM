#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'ftdi.uart' (provides UART comms with FTDI based interfaces).
# (C) 2014-2017 CeDeROM Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import pylibftdi

interfaces = {
    'Custom': {'vid': 0x0000, 'pid': 0x0000, 'uart_interface': ''},
    'KT-LINK': {'vid': 0x0403, 'pid': 0xbbe2, 'uart_interface': 2}
}


class module(object):
    """
    Provides UART comms with FTDI based interfaces.
    """

    def __init__(self, **params):
        """Create FTDI UART Device.
        Note: Use Setup routine to connect to a physical Device.
        """
        self.name = 'ftdi.uart'
        if not 'iCeDeROM' in params:
            raise KeyError('iCeDeROM parameter reference mandatory!')
        self.iCeDeROM = params['iCeDeROM']
        self.capabilities = ['uart']
        self.isSetup = False
        self.ui = dict()
        self.devcfg = dict()
        self.parent = None
        self.baudrates = [300, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200, 230400]
        # Try to run GUI if possible
        if self.iCeDeROM.ui == 'qt':
            import iCeDeROM.interface.ftdi_qt as ftdi_qt
            params['parent'] = self
            self.ui['qt'] = ftdi_qt.module(**params)

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
        cfg = dict()
        try:
            if 'vid' in params:
                if type(params['vid']) == type('a'):
                    params['vid'] = int(params['vid'], base=16)
                    self.devcfg['vid'] = params['vid']
                if pylibftdi.USB_VID_LIST.count(params['vid']) == 0:
                    pylibftdi.USB_VID_LIST.append(params['vid'])
            if 'pid' in params:
                if type(params['pid']) == type('a'):
                    params['pid'] = int(params['pid'], base=16)
                    self.devcfg['pid'] = params['pid']
                if pylibftdi.USB_PID_LIST.count(params['pid']) == 0:
                    pylibftdi.USB_PID_LIST.append(params['pid'])
            if 'serial' in params:
                if params['serial'] != '':
                    cfg['device_id'] = params['serial']
            if 'channel' in params:
                cfg['interface_select'] = params['channel']
            if 'mode' in params:
                mode = params['mode']
                if str(mode).lower()[0] == 't':
                    cfg['mode'] = params['mode'] = 't'
                else:
                    cfg['mode'] = params['mode'] = 'b'
            if 'encoding' in params:
                cfg['encoding'] = params['encoding']
            if 'index' in params:
                index = int(params['index'])
                if index > 0:
                    cfg['device_index'] = index
            if 'interface' in params:
                cfg['interface_select'] = int(params['interface'])
        except:
            self.iCeDeROM.modules['log'].log.exception('Invalid FTDI UART configuration!')
            if 'gui' in self.iCeDeROM.modules:
                self.iCeDeROM.modules['gui'].dialogs['message'].critical(
                    params['iCeDeROM'].modules['gui'].window,
                    'FTDI UART Interface', 'Invalid FTDI UART Interface confguration!')
            return False
        # Connect to the device
        try:
            self.device = pylibftdi.Device(**cfg)
        except:
            self.iCeDeROM.modules['log'].log.exception('FTDI UART Interface setup failed!')
            if 'gui' in self.iCeDeROM.modules:
                self.iCeDeROM.modules['gui'].dialogs['message'].critical(
                    params['iCeDeROM'].modules['gui'].window,
                    'FTDI UART Interface', 'FTDI UART Interface setup failed!')
            return False
        if 'mode' in params:
            self.devcfg['mode'] = params['mode']
        if 'baudrate' in params:
            self.devcfg['baudrate'] = int(params['baudrate'])
            self.device.baudrate = self.devcfg['baudrate']
        self.iCeDeROM.modules['log'].log.info('FTDI UART Interface connected: vid=' +
                                              hex(self.devcfg['vid']) + ' pid=' + hex(
            self.devcfg['pid']) + ' cfg=' + str(cfg))
        # TODO verify set default method
        self.iCeDeROM.modules['gui'].labels['interface'].setText(self.name)
        self.iCeDeROM.modules['interface'].device = self

    def start(self, **params):
        if 'qt' in self.ui:
            self.ui['qt'].start(**params)

    def stop(self, **params):
        if 'qt' in self.ui:
            self.ui['qt'].stop(**params)

    def write(self, data):
        self.device.write(data)

    def read(self, length):
        return self.device.read(length)
