#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'Terminal' (terminal module for shell and/or serial port).
# (C) 2014-2017 CeDeROM Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

class module(object):
    """Terminal Module with Qt mdiChild window."""

    def __init__(self, **params):
        """
        Create Module and QtWidget if necessary.
        Parameters:
            iCeDeROM module reference (mandatory).
        """
        self.name = 'terminal'
        if not 'iCeDeROM' in params:
            raise KeyError('iCeDeROM parameter reference mandatory!')
        self.iCeDeROM = params['iCeDeROM']
        self.ui = dict()
        self.logFile = False
        self.logFileEnabled = False
        self.logFile = None
        self.logFileName = self.iCeDeROM.path
        self.logFileName += '/' + 'iCeDeROM-Terminal-Dump.txt'
        if self.iCeDeROM.ui == 'qt':
            from iCeDeROM.cli import terminal_qt
            params['parent'] = self
            self.ui['qt'] = terminal_qt.module(**params)
            self.ui['qt'].parent = self

    def setup(self, **params):
        if self.iCeDeROM.ui == 'qt':
            self.ui['qt'].setup(**params)

    def start(self, **params):
        if self.iCeDeROM.ui == 'qt':
            self.ui['qt'].start(**params)

    def stop(self, **params):
        if self.iCeDeROM.ui == 'qt':
            self.ui['qt'].stop(**params)

    def write(self, data):
        self.iCeDeROM.modules['interface'].write(data)
        self.logFileWrite(data)

    def read(self, length):
        chunk = self.iCeDeROM.modules['interface'].read(length)
        if chunk != '': self.logFileWrite(chunk)
        return chunk

    def logFileStart(self, filename):
        if self.logFileEnabled: self.logFileStop()
        if filename != self.logFileName: self.logFileName = filename
        try:
            self.logFile = open(self.logFileName, 'w+b')
        except:
            self.iCeDeROM.modules['log'].log.exception('Cannot open log file for writing!')
            if self.iCeDeROM.ui == 'qt':
                self.iCeDeROM.modules['gui'].dialogs['message'].warning(
                    self.iCeDeROM.modules['gui'].window,
                    'Terminal Log File', 'Cannot open log file for writing!')
        self.logFileEnabled = True
        self.iCeDeROM.modules['log'].log.info('Terminal streams to: ' + self.logFileName)

    def logFileStop(self):
        if not self.logFile: return
        self.logFile.flush()
        self.logFile.close()
        self.logFileEnabled = False

    def logFileWrite(self, data):
        #TODO: FIX HARDCODED UTF ENCODING / ADD TERMINAL ENCODING
        if self.logFileEnabled: self.logFile.write(bytearray(source=data, encoding="UTF-8"))
