#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'Memory' (memory buffer module to store data).
# (C) 2014-2017 CeDeROM Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import io

default_filename = 'iCeDeROM.membuf'
default_chunksize = io.DEFAULT_BUFFER_SIZE


class module(object):
    """Memory Core Module that holds analysis data."""

    def __init__(self, **params):
        """
		Create Module and QtWidget if necessary.
		Parameters:
			iCeDeROM module reference (mandatory).
		"""
        self.name = 'memory'
        if not 'iCeDeROM' in params:
            raise KeyError('iCeDeROM parameter reference mandatory!')
        self.iCeDeROM = params['iCeDeROM']
        self.buffer = None
        self.filename = None
        self.chunksize = default_chunksize
        self.chunkdata = None
        self.size = 0
        self.ui = dict()
        if self.iCeDeROM.ui == 'qt':
            from iCeDeROM.memory import memory_qt
            params['parent'] = self
            self.ui['qt'] = memory_qt.module(**params)
        self.fileOpen(self.iCeDeROM.path + '/' + default_filename)

    def setup(self, **params):
        if self.iCeDeROM.ui == 'qt':
            self.ui['qt'].setup(**params)

    def start(self, **params):
        if self.iCeDeROM.ui == 'qt':
            self.ui['qt'].start(**params)

    def stop(self, **params):
        if self.iCeDeROM.ui == 'qt':
            self.ui['qt'].stop(**params)

    def fileOpen(self, filename=default_filename):
        self.iCeDeROM.modules['log'].log.info('Loading file: ' + filename)
        if self.filename != None: self.buffer.close()
        try:
            self.buffer = io.open(filename, mode='a+', buffering=self.chunksize)
            self.size = self.buffer.seek(0, io.SEEK_END)
            self.filename = filename
            if 'qt' in self.ui:
                self.ui['qt'].window.statusBar().showMessage(str(self.filename))
        except:
            self.iCeDeROM.modules['log'].log.exception('Error opening file!')
            self.iCeDeROM.modules['gui'].dialogs['message'].warning(
                self.iCeDeROM.modules['gui'].window,
                'Error', 'Error opening file!\n' + str(filename))

    def fileSave(self, filename):
        if self.filename == None: return
        if filename == self.filename:
            self.buffer.flush()
        else:
            try:
                newbuffer = io.open(filename, mode='w+b')
                self.buffer.seek(0, io.SEEK_SET)
                newbuffer.write(self.buffer.read())
            except:
                self.iCeDeROM.modules['log'].log.exception('Error saving new file!')
                if 'qt' in self.ui:
                    self.iCeDeROM.modules['gui'].dialogs['message'].warning(
                        self.iCeDeROM.modules['gui'].window,
                        'Error', 'Error saving new file!\n' + str(self.filename))
            self.buffer.close()
            self.buffer = newbuffer
            if 'qt' in self.ui:
                self.ui['qt'].window.statusBar().showMessage(str(self.filename))

    def fileClose(self):
        try:
            self.buffer.close()
            if 'qt' in self.ui:
                self.ui['qt'].window.statusBar().showMessage('')
        except:
            self.iCeDeROM.modules['log'].log.exception('Error closing file!')
            if 'qt' in self.ui:
                self.iCeDeROM.modules['gui'].dialogs['message'].warning(
                    self.iCeDeROM.modules['gui'].window,
                    'Error', 'Error closing file!\n' + str(self.filename))
