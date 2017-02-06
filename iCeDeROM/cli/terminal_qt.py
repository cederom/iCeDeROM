#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'terminal_qt' (provides QtWidget for modules.cli.terminal iCeDeROM Module.
# (C) 2014-2017 CeDeROM Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import os
from PyQt5 import QtCore, QtWidgets


class module(object):
    """
	Provides Qt Widget for modules.cli.terminal iCeDeROM module.
	"""

    def __init__(self, **params):
        """Create Qt Widget for Terminal CLI."""
        self.name = 'terminal_qt'
        if not 'iCeDeROM' in params:
            raise KeyError('iCeDeROM parameter reference mandatory!')
        if not 'gui' in params['iCeDeROM'].modules:
            raise RuntimeError('Terminal QtWidget requires GUI running!')
        self.iCeDeROM = params['iCeDeROM']
        self.parent = params['parent'] if 'parent' in params else None
        self.windows = dict()
        self.texts = dict()
        self.fonts = dict()
        self.layouts = dict()
        self.menus = dict()
        self.actions = dict()
        self.tabs = dict()
        self.groups = dict()
        self.trees = dict()
        self.buttons = dict()
        self.logFileName = self.parent.logFileName
        self.createQtWidget(**params)
        self.setupQtWidget(**params)

    def setup(self, **params):
        return

    def start(self, **params):
        if self.iCeDeROM.ui != 'qt':
            raise RuntimeError('Interface QtWidget requires Qt GUI running!')
        self.iCeDeROM.modules['gui'].mdi.addSubWindow(self.windows[self.name])
        self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(False)
        self.tabs['config_id'] = self.iCeDeROM.modules['gui'].tabs['system'].addTab(self.tabs['config'], 'Terminal')
        self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(True)
        self.windows[self.name].show()

    def stop(self, **params):
        if self.iCeDeROM.ui != 'qt':
            raise RuntimeError('Interface QtWidget requires Qt GUI running!')
        self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(False)
        self.iCeDeROM.modules['gui'].tabs['system'].delTab(self.tabs['config_id'])
        self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(True)
        self.windows[self.name].hide()

    def createQtWidget(self, **params):
        if self.iCeDeROM.ui != 'qt':
            raise Warning('Interface QtWidget requires Qt GUI running!')
        self.createQtWidgetMdiWindow(**params)
        self.createQtWidgetMenu(**params)
        self.createQtWidgetConfigTab(**params)

    def createQtWidgetMdiWindow(self, **params):
        self.windows[self.name] = QtWidgets.QMainWindow()
        self.texts[self.name] = QtWidgets.QTextEdit(self.windows[self.name])

    # TODO: FIX COMPONENT CODE
    # self.fonts[self.name]=QtWidgets.QFont('courier')

    def createQtWidgetMenu(self, **params):
        self.menus[self.name] = QtWidgets.QMenu('Terminal')
        self.menus['window'] = QtWidgets.QMenu('Window')

    def createQtWidgetConfigTab(self, **params):
        self.tabs['config'] = QtWidgets.QTabWidget()
        self.layouts['terminal_config'] = QtWidgets.QVBoxLayout(self.tabs['config'])
        self.groups['config'] = QtWidgets.QGroupBox('Terminal Configuration')
        self.layouts['config'] = QtWidgets.QVBoxLayout(self.groups['config'])
        self.trees['config'] = QtWidgets.QTreeWidget()

    def setupQtWidget(self, **params):
        if self.iCeDeROM.ui != 'qt':
            raise Warning('Interface QtWidget requires Qt GUI running!')
        self.setupQtWidgetMdiWindow(**params)
        self.setupQtWidgetMenu(**params)
        self.setupQtWidgetConfigTab(**params)

    def setupQtWidgetMdiWindow(self, **params):
        self.windows[self.name].setWindowTitle('Terminal')
        self.windows[self.name].setCentralWidget(self.texts[self.name])
        self.windows[self.name].statusBar()
        self.texts[self.name].setReadOnly(False)
        # TODO: FIX COMPONENT CODE / SEE ABOVE FONT INIT
        # self.texts[self.name].setFont(self.fonts[self.name])
        self.texts[self.name].setAcceptRichText(False)
        self.texts[self.name].keyPressEvent = self.keyPressEvent
        self.texts[self.name].insertFromMimeData = self.insertFromMimeData
        self.texts[self.name].startTimer(0)
        self.texts[self.name].timerEvent = self.timerEvent

    def setupQtWidgetMenu(self, **params):
        self.actions['window_show'] = self.menus['window'].addAction('Show', self.windowShow)
        self.actions['window_hide'] = self.menus['window'].addAction('Hide', self.windowHide)
        self.menus[self.name].addMenu(self.menus['window'])
        self.iCeDeROM.modules['gui'].menus['modules'].addMenu(self.menus[self.name])

    def setupQtWidgetConfigTab(self, **params):
        self.layouts['terminal_config'].addWidget(self.groups['config'])
        self.groups['config'].setLayout(self.layouts['config'])
        self.layouts['config'].addWidget(self.trees['config'])
        self.layouts['config'].setContentsMargins(0, 0, 0, 0)
        self.layouts['config'].setSpacing(0)
        self.trees['config'].setMinimumHeight(100)
        self.trees['config'].setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum))
        # Populate the TreeWidget
        self.trees['config'].setHeaderItem(QtWidgets.QTreeWidgetItem(
            ['parameter', 'value', 'descrption']))
        self.trees['config'].setColumnWidth(0, 150)
        self.trees['config'].setColumnWidth(1, 100)
        # LogFile branch
        self.trees['logfile'] = QtWidgets.QTreeWidgetItem(self.trees['config'], ['LogFile'])
        self.trees['logtofile'] = QtWidgets.QTreeWidgetItem(self.trees['logfile'],
                                                            ['Log To File', '',
                                                             'Stream Terminal data to a local file.'])
        self.buttons['logtofile'] = QtWidgets.QCheckBox()
        self.buttons['logtofile'].setTristate(False)
        # TODO: FIX SIGNALLING CODE
        # self.buttons['logtofile'].connect(
        #	self.buttons['logtofile'],QtCore.SIGNAL('stateChanged(int)'),self.logFileToggle)
        self.trees['config'].setItemWidget(self.trees['logtofile'], 1, self.buttons['logtofile'])
        self.trees['logfilename'] = QtWidgets.QTreeWidgetItem(self.trees['logfile'],
                                                              ['Filename', '', self.logFileName])
        self.buttons['logfilename'] = QtWidgets.QPushButton('Select')
        self.trees['config'].setItemWidget(self.trees['logfilename'], 1, self.buttons['logfilename'])
        # TODO: FIX SIGNALLING CODE
        # self.buttons['logfilename'].connect(
        #	self.buttons['logfilename'],QtCore.SIGNAL('clicked()'),self.logFileSelect)
        # Display branch
        self.trees['display'] = QtWidgets.QTreeWidgetItem(self.trees['config'], ['Display'])
        self.trees['autoscroll'] = QtWidgets.QTreeWidgetItem(self.trees['display'],
                                                             ['Auto Scroll', '',
                                                              'Scroll the window when new data arrives.'])
        self.buttons['autoscroll'] = QtWidgets.QCheckBox()
        self.buttons['autoscroll'].setChecked(True)
        self.trees['config'].setItemWidget(self.trees['autoscroll'], 1, self.buttons['autoscroll'])
        self.trees['clear'] = QtWidgets.QTreeWidgetItem(self.trees['display'],
                                                        ['Clear', '', 'Crear Terminal.'])
        self.buttons['clear'] = QtWidgets.QPushButton('Clear')
        # TODO: FIX SIGNALLIG CODE
        # self.buttons['clear'].connect(self.buttons['clear'],QtCore.SIGNAL('clicked()'),self.clearTerminal)
        self.trees['config'].setItemWidget(self.trees['clear'], 1, self.buttons['clear'])
        self.trees['config'].expandAll()

    def logFileToggle(self):
        if self.buttons['logtofile'].isChecked():
            if os.access(self.logFileName, os.F_OK):
                res = self.iCeDeROM.modules['gui'].dialogs['message'].information(
                    self.iCeDeROM.modules['gui'].window,
                    'File Question', 'File already exist! Do you want to overwrite?',
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if res == QtWidgets.QMessageBox.No:
                    self.buttons['logtofile'].setChecked(False)
                    return
            self.parent.logFileStart(self.logFileName)
            self.parent.logFileWrite(str(self.texts[self.name].toPlainText()))
            self.windows[self.name].statusBar().showMessage(
                'Stream: ' + self.logFileName)
        else:
            self.parent.logFileStop()
            self.windows[self.name].statusBar().showMessage('')

    def logFileSelect(self):
        filename = self.iCeDeROM.modules['gui'].dialogs['file'].getSaveFileName(
            self.iCeDeROM.modules['gui'].window, 'Save File')
        if filename == '': return
        self.logFileName = str(filename)
        self.trees['logfilename'].setText(2, self.logFileName)

    def keyPressEvent(self, QKeyEvent):
        '''Handle keystrokes.'''
        if self.iCeDeROM.modules['interface'].device == None: return
        try:
            self.parent.write(QKeyEvent.text())
        except:
            self.iCeDeROM.modules['log'].log.exception('Write failed!')

    def insertFromMimeData(self, QMimeData):
        '''Handle Paste-From-Clipboard and Drag-And-Drop.'''
        if self.iCeDeROM.modules['interface'].device == None: return
        try:
            self.parent.write(QMimeData.text())
        except:
            self.iCeDeROM.modules['log'].log.exception('Paste failed!')

    def timerEvent(self, QTimerEvent):
        if self.iCeDeROM.modules['interface'].device == None: return
        self.write(self.parent.read(32))

    def write(self, data):
        if data == '': return
        self.texts[self.name].insertPlainText(data)
        if self.buttons['autoscroll'].isChecked():
            self.texts[self.name].moveCursor(QtWidgets.QTextCursor.End, QtWidgets.QTextCursor.MoveAnchor)

    def clearTerminal(self):
        self.texts[self.name].setPlainText('')

    def windowShow(self):
        self.windows[self.name].show()

    def windowHide(self):
        self.windows[self.name].hide()
