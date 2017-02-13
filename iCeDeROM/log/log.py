#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'log' (provides logging capabilities).
# (C) 2014-2017 CeDeROM Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import logging
import sys, io
from PyQt5 import QtCore, QtWidgets

default_filename = 'iCeDeROM.log'
default_level = logging.INFO
default_format = '%(asctime)s %(levelname)s %(filename)s/%(funcName)s: %(message)s'


class module(object):
    """
    Provides basic logging capabilities (based on the python 'logging' module).
    Two outputs are provided: Stream(sys.stderr), File(filename='iCeDeROM.log').
    External modules can read log information from Stream and/or File as needed.
    """

    def __init__(self, **params):
        """Creates logger."""
        self.name = 'log'
        if not 'iCeDeROM' in params:
            raise KeyError('iCeDeROM parameter reference mandatory!')
        self.iCeDeROM = params['iCeDeROM']
        self.texts = dict()
        self.log = logging.getLogger('iCeDeROM')
        self.filename = default_filename
        self.level = default_level
        self.format = default_format

    def start(self, **params):
        return

    def stop(self, **params):
        logging.shutdown()

    def setup(self, **params):
        """
        Setup the Logger (Formatter, StreamHandler, FileHandler, LogLevel).
        Parameters:
            filename where logs should go.
            format   of the logged messages.
            level    is the default loglevel.
        If parameter is not provided a default value is used.
        """
        self.filename = params['filename'] if 'filename' in params else default_filename
        self.level = params['level'] if 'level' in params else default_level
        self.format = params['format'] if 'format' in params else default_format
        self.setupFormatter(self.format)
        self.setupStreamHandler(self.level)
        self.setupFileHandler(self.filename, self.level)
        self.setupLevel(self.level)

    def setupFormatter(self, format=default_format):
        """
        Setup the Formatter.
        Parameters:
            format   of the logged messages.
        If parameter is not provided a default value is used.
        """
        self.formatter = logging.Formatter(format)

    def setupStreamHandler(self, level=default_level):
        """
        Setup the StreamHandler. sys.STDERR is the output.
        Parameters:
            level    is the default loglevel.
        If parameter is not provided a default value is used.
        """
        self.stream = logging.StreamHandler()
        self.stream.setLevel(level)
        self.stream.setFormatter(self.formatter)
        self.log.addHandler(self.stream)

    def setupFileHandler(self, filename=default_filename, level=default_level, mode='w'):
        """
        Setup the FileHandler.
        Parameters:
            filename where logs should go.
            level    is the default loglevel.
        If parameter is not provided a default value is used.
        """
        self.file = logging.FileHandler(filename, mode)
        self.file.setLevel(level)
        self.file.setFormatter(self.formatter)
        self.log.addHandler(self.file)

    def setupLevel(self, level=default_level):
        """
        Setup the LogLevel).
        Parameters:
            level    is the default loglevel.
        If parameter is not provided a default value is used.
        """
        self.log.setLevel(level)
        self.stream.setLevel(level)
        self.file.setLevel(level)

    def createQtWidget(self, **params):
        self.texts[self.name] = QtWidgets.QTextEdit()
        self.texts[self.name].setAcceptRichText(False)
        self.texts[self.name].setReadOnly(True)
        self.texts[self.name].setFontFamily("Courier")
        self.texts[self.name].show()
        self.logfswatcher = QtCore.QFileSystemWatcher([self.filename])
        # TODO: FIX SIGNALS CODE
        # self.logfswatcher.connect(self.logfswatcher, QtCore.SIGNAL('fileChanged(QString)'),self.logFileWatcher)
        self.logfp = io.open(self.filename, 'rt')
        self.logfswatcher.fileChanged['QString'].connect(self.logFileWatcher)

        return self.texts[self.name]

    @QtCore.pyqtSlot(str)
    def logFileWatcher(self, path):
        self.texts[self.name].insertPlainText(self.logfp.read())
