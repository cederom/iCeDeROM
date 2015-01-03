#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'python_qt' (provides QtWidget for modules.cli.python iCeDeROM module.
# (C) 2014-2015 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

from PyQt4 import QtCore,QtGui

class module(QtGui.QTextEdit):
	"""
	Provides Qt Widget for modules.cli.python iCeDeROM module.
	"""
	def __init__(self, **params):
		"""Create Qt Widget for Python CLI."""
		self.name='cli_python_qt'		
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if not params['iCeDeROM'].modules.has_key('gui'):
			raise RuntimeError('Python Console QtWidget requires GUI running!')
		self.iCeDeROM=params['iCeDeROM']
		super(module, self).__init__()		
		self.tabs=dict()		
		self.setAcceptRichText(False)
		self.setReadOnly(False)
		self.setFontFamily("Courier")
		self.history_index=0
		self.history=list()

	def setup(self, **params):
		return
	
	def start(self, **params):
		self.show()
	
	def stop(self, **params):
		self.hide()

	def keyPressEvent(self, QKeyEvent):
		cursor=self.textCursor()
		if QKeyEvent.key()==QtCore.Qt.Key_Return:
			cursor.select(QtGui.QTextCursor.LineUnderCursor)
			self.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
			self.setTextCursor(cursor)
			self.command=unicode(self.textCursor().selectedText())
			self.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
			self.insertPlainText('\n')
			self.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
			self.historyAppend(self.command)
			self.execute(self.command)
		elif QKeyEvent.key()==QtCore.Qt.Key_Up:
			if self.history_index>0: self.history_index-=1
			cursor.select(QtGui.QTextCursor.LineUnderCursor)
			self.setTextCursor(cursor)
			self.insertPlainText(self.history[self.history_index])
		elif QKeyEvent.key()==QtCore.Qt.Key_Down:
			if self.history_index<len(self.history)-1: self.history_index+=1
			cursor.select(QtGui.QTextCursor.LineUnderCursor)
			self.setTextCursor(cursor)
			self.insertPlainText(self.history[self.history_index])			
		elif QKeyEvent.key()==QtCore.Qt.Key_PageUp:
			self.history_index=0
			cursor.select(QtGui.QTextCursor.LineUnderCursor)
			self.setTextCursor(cursor)			
			self.insertPlainText(self.history[self.history_index])
		elif QKeyEvent.key()==QtCore.Qt.Key_PageDown:
			self.history_index=len(self.history)-1
			cursor.select(QtGui.QTextCursor.LineUnderCursor)
			self.setTextCursor(cursor)			
			self.insertPlainText(self.history[self.history_index])			
		else:
			super(module, self).keyPressEvent(QKeyEvent)		

	def write(self, data):
		self.insertPlainText(data)
		self.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

	def execute(self, command):
		"""Super class should replace this with python evaluation routine."""
		print 'CliPythonQt: No Python handler provided!'

	def historyAppend(self, command):
		if command.strip()=='': return
		self.history.append(command)
		self.history_index=len(self.history)
		
