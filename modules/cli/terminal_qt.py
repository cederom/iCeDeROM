#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'terminal_qt' (provides QtWidget for modules.cli.terminal iCeDeROM Module.
# (C) 2014-2015 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import os
from PyQt4 import QtCore,QtGui

class module(object):
	"""
	Provides Qt Widget for modules.cli.terminal iCeDeROM module.
	"""
	def __init__(self, **params):
		"""Create Qt Widget for Terminal CLI."""
		self.name='terminal_qt'		
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		if not params['iCeDeROM'].modules.has_key('gui'):
			raise RuntimeError('Terminal QtWidget requires GUI running!')
		self.iCeDeROM=params['iCeDeROM']
		self.parent=params['parent'] if params.has_key('parent') else None
		self.windows=dict()
		self.texts=dict()
		self.fonts=dict()
		self.layouts=dict()
		self.menus=dict()
		self.actions=dict()
		self.tabs=dict()
		self.groups=dict()
		self.trees=dict()
		self.buttons=dict()
		self.logFileEnabled=False
		self.logFileName=self.parent.logFileName
		self.createQtWidget(**params)
		self.setupQtWidget(**params)

	def setup(self, **params):	
		return
	
	def start(self, **params):
		if self.iCeDeROM.ui!='qt':
			raise RuntimeError('Interface QtWidget requires Qt GUI running!')					
		self.iCeDeROM.modules['gui'].mdi.addSubWindow(self.windows[self.name])
		self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(False)
		self.tabs['config_id']=self.iCeDeROM.modules['gui'].tabs['system'].addTab(self.tabs['config'], 'Terminal')
		self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(True)		
		self.windows[self.name].show()
	
	def stop(self, **params):
		if self.iCeDeROM.ui!='qt':
			raise RuntimeError('Interface QtWidget requires Qt GUI running!')	
		self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(False)
		self.iCeDeROM.modules['gui'].tabs['system'].delTab(self.tabs['config_id'])
		self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(True)		
		self.windows[self.name].hide()

	def createQtWidget(self, **params):
		if self.iCeDeROM.ui!='qt':
			raise Warning('Interface QtWidget requires Qt GUI running!')
		self.createQtWidgetMdiWindow(**params)
		self.createQtWidgetMenu(**params)
		self.createQtWidgetConfigTab(**params)

	def createQtWidgetMdiWindow(self, **params):
		self.windows[self.name]=QtGui.QMainWindow()
		self.texts[self.name]=QtGui.QTextEdit(self.windows[self.name])
		self.fonts[self.name]=QtGui.QFont('courier')

	def createQtWidgetMenu(self, **params):
		self.menu=QtGui.QMenu('Terminal')

	def createQtWidgetConfigTab(self, **params):
		self.tabs['config']=QtGui.QTabWidget()
		self.layouts['terminal_config']=QtGui.QVBoxLayout(self.tabs['config'])
		self.groups['config']=QtGui.QGroupBox('Terminal Configuration')
		self.layouts['config']=QtGui.QVBoxLayout(self.groups['config'])
		self.trees['config']=QtGui.QTreeWidget()

	def setupQtWidget(self, **params):
		if self.iCeDeROM.ui!='qt':
			raise Warning('Interface QtWidget requires Qt GUI running!')		
		self.setupQtWidgetMdiWindow(**params)
		self.setupQtWidgetMenu(**params)
		self.setupQtWidgetConfigTab(**params)

	def setupQtWidgetMdiWindow(self, **params):
		self.windows[self.name].setWindowTitle('Terminal')
		self.windows[self.name].setCentralWidget(self.texts[self.name])
		self.texts[self.name].setReadOnly(False)
		self.texts[self.name].setFont(self.fonts[self.name])
		self.texts[self.name].setAcceptRichText(False)		
		self.texts[self.name].keyPressEvent=self.keyPressEvent
		self.texts[self.name].insertFromMimeData=self.insertFromMimeData
		self.texts[self.name].startTimer(0)
		self.texts[self.name].timerEvent=self.timerEvent
		
	def setupQtWidgetMenu(self, **params):
		self.actions['source']=self.menu.addAction('Test',self.test)
		self.iCeDeROM.modules['gui'].menus['modules'].addMenu(self.menu)

	def setupQtWidgetConfigTab(self, **params):
		self.layouts['terminal_config'].addWidget(self.groups['config'])
		self.groups['config'].setLayout(self.layouts['config'])
		self.layouts['config'].addWidget(self.trees['config'])
		self.layouts['config'].setContentsMargins(0,0,0,0)		
		self.layouts['config'].setSpacing(0)
		self.trees['config'].setMinimumHeight(100)
		self.trees['config'].setSizePolicy(QtGui.QSizePolicy(
			QtGui.QSizePolicy.Minimum,
			QtGui.QSizePolicy.Minimum))
		#Populate the TreeWidget
		self.trees['config'].setHeaderItem(QtGui.QTreeWidgetItem(
			['parameter','value','descrption']))
		self.trees['config'].setColumnWidth(0,150)
		self.trees['config'].setColumnWidth(1,100)
		#DEVICE branch
		self.trees['logfile']=QtGui.QTreeWidgetItem(self.trees['config'], ['LogFile'])
		self.trees['logtofile']=QtGui.QTreeWidgetItem(self.trees['logfile'],
			['Log To File','','Stream Terminal data to a local file.'])
		self.buttons['logtofile']=QtGui.QCheckBox()
		self.buttons['logtofile'].connect(
			self.buttons['logtofile'],QtCore.SIGNAL('stateChanged(int)'),self.logFileToggle)
		self.trees['config'].setItemWidget(self.trees['logtofile'],1,self.buttons['logtofile'])
		self.trees['logfilename']=QtGui.QTreeWidgetItem(self.trees['logfile'],
			['Filename','',self.logFileName])
		self.buttons['logfilename']=QtGui.QPushButton('Select')
		self.trees['config'].setItemWidget(self.trees['logfilename'],1,self.buttons['logfilename'])
		self.buttons['logfilename'].connect(
			self.buttons['logfilename'],QtCore.SIGNAL('clicked()'),self.logFileSelect)
		
		self.trees['config'].expandAll()


	def logFileToggle(self):
		if self.buttons['logtofile'].isChecked():
			if os.access(self.logFileName,os.F_OK):
				res=self.iCeDeROM.modules['gui'].dialogs['message'].information(
					self.iCeDeROM.modules['gui'].window,
					'File Question', 'File already exist! Do you want to overwrite?',
					QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
				if res==QtGui.QMessageBox.Yes:
					print 'WRITING\n'
					self.parent.logFileStart(self.logFileName)
		else:
			self.parent.logFileStop()

	def logFileSelect(self):
		filename=self.iCeDeROM.modules['gui'].dialogs['file'].getSaveFileName(
			self.iCeDeROM.modules['gui'].window,'Save File')
		if filename=='': return
		self.logFileName=str(filename)
		self.trees['logfilename'].setText(2,self.logFileName)
		
	def keyPressEvent(self, QKeyEvent):
		'''Handle keystrokes.'''
		if self.iCeDeROM.modules['interface'].device==None: return
		try:
			self.parent.write(QKeyEvent.text())
		except:
			self.iCeDeROM.modules['log'].log.exception('Write failed!')

	def insertFromMimeData(self, QMimeData):
		'''Handle Paste-From-Clipboard and Drag-And-Drop.'''
		if self.iCeDeROM.modules['interface'].device==None: return
		try:
			self.parent.write(QMimeData.text())
		except:
			self.iCeDeROM.modules['log'].log.exception('Paste failed!')		

	def timerEvent(self, QTimerEvent):
		if self.iCeDeROM.modules['interface'].device==None: return
		self.write(self.parent.read(32))

	def write(self, data):
		if data=='': return
		self.texts[self.name].insertPlainText(data)
		self.texts[self.name].moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
		
	def test(self):
		self.iCeDeROM.modules['gui'].dialogs['message'].information(self,'Terminal','This is a Terminal Menu Test...')
