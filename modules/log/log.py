#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'log' (provides logging capabilities).
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import logging

default_filename='iCeDeROM.log'
default_level=logging.INFO
default_format='%(asctime)s %(levelname)s %(filename)s/%(funcName)s: %(message)s'

class module(object):
	"""Provides basic logging capabilities (based on the python 'logging' module)."""
	def __init__(self, **params):
		"""Creates logger."""
		self.name='log'
		self.log=logging.getLogger('iCeDeROM')

	def setup(self, **params):
		"""
		Setup the Logger (Formatter, StreamHandler, FileHandler, LogLevel).
		Parameters:
			filename where logs should go.
			format   of the logged messages.
			level    is the default loglevel.
		If parameter is not provided a default value is used.
		"""
		filename=params['filename'] if params.has_key('filename') else default_filename
		level=params['level'] if params.has_key('level') else default_level
		format=params['format'] if params.has_key('format') else default_format
		self.setupFormatter(format)
		self.setupStreamHandler(level)
		self.setupFileHandler(filename, level)
		self.setupLevel(level)


	def setupFormatter(self, format=default_format):
		"""
		Setup the Formatter.
		Parameters:
			format   of the logged messages.
		If parameter is not provided a default value is used.
		"""		
		self.formatter=logging.Formatter(format)

	def setupStreamHandler(self, level=default_level):
		"""
		Setup the StreamHandler.
		Parameters:
			level    is the default loglevel.
		If parameter is not provided a default value is used.
		"""		
		self.stream=logging.StreamHandler()
		self.stream.setLevel(level)
		self.stream.setFormatter(self.formatter)
		self.log.addHandler(self.stream)

	def setupFileHandler(self, filename=default_filename, level=default_level):
		"""
		Setup the FileHandler.
		Parameters:
			filename where logs should go.
			level    is the default loglevel.
		If parameter is not provided a default value is used.
		"""		
		self.file=logging.FileHandler(filename)
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
