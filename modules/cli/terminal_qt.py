#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'terminal_qt' (provides QtWidget for modules.cli.terminal iCeDeROM Module.
# (C) 2014-2015 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

from PyQt4 import QtCore,QtGui

class module(QtGui.QWidget):
	"""
	Provides Qt Widget for modules.cli.terminal iCeDeROM module.
	"""
	def __init__(self, **params):
		"""Create Qt Widget for Terminal CLI."""
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if not params['iCeDeROM'].modules.has_key('gui'):
			raise KeyError('Terminal QtWidget requires GUI running!')
		super(module, self).__init__()
		self.name='terminal_qt'
		self.iCeDeROM=params['iCeDeROM']
		self.parent=None
		self.texts=dict()
		self.layouts=dict()
		self.menus=dict()
		self.actions=dict()
		self.createQtWidget(**params)
		self.setupQtWidget(**params)

	def setup(self, **params):	
		return
	
	def start(self, **params):
		self.iCeDeROM.modules['gui'].mdi.addSubWindow(self)
		self.show()
	
	def stop(self, **params):
		self.hide()

	def createQtWidget(self, **params):
		self.layouts[self.name]=QtGui.QVBoxLayout(self)
		self.texts[self.name]=QtGui.QPlainTextEdit()
		self.menu=QtGui.QMenu('Terminal')

	def setupQtWidget(self, **params):
		self.setWindowTitle('Terminal')
		self.layouts[self.name].setContentsMargins(0,0,0,0)
		self.layouts[self.name].addWidget(self.texts[self.name])
		self.texts[self.name].setReadOnly(False)
		self.texts[self.name].keyPressEvent=self.keyPressEvent
		self.texts[self.name].startTimer(0)
		self.texts[self.name].timerEvent=self.timerEvent
		self.actions['source']=self.menu.addAction('Test',self.test)
		self.iCeDeROM.modules['gui'].menus['modules'].addMenu(self.menu)
		
	def keyPressEvent(self, QKeyEvent):
		if self.iCeDeROM.modules['interface'].device==None: return
		try:
			self.parent.write(QKeyEvent.text())
		except:
			self.iCeDeROM.modules['log'].log.exception('Write failed!')

	def timerEvent(self, QTimerEvent):
		if self.iCeDeROM.modules['interface'].device==None: return
		self.write(self.iCeDeROM.modules['interface'].device.read(128))

	def write(self, data):
		self.texts[self.name].insertPlainText(data)
		self.texts[self.name].moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
		
	def test(self):
		self.iCeDeROM.modules['gui'].dialogs['message'].information(self,'Terminal','This is a Terminal Menu Test...')
