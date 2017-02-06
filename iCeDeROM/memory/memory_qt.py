#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'memory_qt' (provides QtWidget for Memory iCeDeROM Module.
# (C) 2014-2017 CeDeROM Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

from PyQt5 import QtCore, QtWidgets


class module(object):
    """
	Provides Qt Widget for Memory iCeDeROM module.
	"""

    def __init__(self, **params):
        """Create Qt Widget for Memory module."""
        self.name = 'memory_qt'
        if not 'iCeDeROM' in params:
            raise KeyError('iCeDeROM parameter reference mandatory!')
        if not 'gui' in params['iCeDeROM'].modules:
            raise RuntimeError('Memory QtWidget requires GUI running!')
        self.iCeDeROM = params['iCeDeROM']
        self.parent = params['parent'] if 'parent' in params else None
        self.windows = dict()
        self.window = None
        self.tables = dict()
        self.tabs = dict()
        self.layouts = dict()
        self.groups = dict()
        self.trees = dict()
        self.buttons = dict()
        self.rows = 0
        self.row_height = 25
        self.hexColumnCount = 16
        self.hexColumnWidth = 25
        self.hexColumnMultiply = 1
        self.addrColumnWidth = 100
        self.asciiColumnWidth = 150
        self.windowContentWidthSingle = self.addrColumnWidth + self.asciiColumnWidth
        self.windowContentWidthSingle += self.hexColumnCount * self.hexColumnWidth
        self.windowContentWidth = self.windowContentWidthSingle
        self.createQtWidget(**params)
        self.setupQtWidget(**params)

    def setup(self, **params):
        return

    def start(self, **params):
        if self.iCeDeROM.ui != 'qt':
            raise RuntimeError('Memory QtWidget requires Qt GUI running!')
        self.iCeDeROM.modules['gui'].mdi.addSubWindow(self.windows[self.name])
        self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(False)
        self.tabs['config_id'] = self.iCeDeROM.modules['gui'].tabs['system'].addTab(self.tabs['config'], 'Memory')
        self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(True)
        self.windows[self.name].show()

    def stop(self, **params):
        if self.iCeDeROM.ui != 'qt':
            raise RuntimeError('Memory QtWidget requires Qt GUI running!')
        self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(False)
        self.iCeDeROM.modules['gui'].tabs['system'].delTab(self.tabs['config_id'])
        self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(True)
        self.windows[self.name].hide()

    def createQtWidget(self, **params):
        if self.iCeDeROM.ui != 'qt':
            raise Warning('Memory QtWidget requires Qt GUI running!')
        self.createQtWidgetMdiWindow(**params)
        self.createQtWidgetConfigTab(**params)

    def createQtWidgetMdiWindow(self, **params):
        self.window = self.windows[self.name] = QtWidgets.QMainWindow()
        self.tables[self.name] = QtWidgets.QTableWidget(self.windows[self.name])

    def createQtWidgetConfigTab(self, **params):
        self.tabs['config'] = QtWidgets.QTabWidget()
        self.layouts['memory_config'] = QtWidgets.QVBoxLayout(self.tabs['config'])
        self.groups['config'] = QtWidgets.QGroupBox('Memory Configuration')
        self.layouts['config'] = QtWidgets.QVBoxLayout(self.groups['config'])
        self.trees['config'] = QtWidgets.QTreeWidget()

    def setupQtWidget(self, **params):
        if self.iCeDeROM.ui != 'qt':
            raise Warning('Interface QtWidget requires Qt GUI running!')
        self.setupQtWidgetMdiWindow(**params)
        self.setupQtWidgetConfigTab(**params)

    def setupQtWidgetMdiWindow(self, **params):
        self.windows[self.name].setWindowTitle('Memory')
        self.windows[self.name].setCentralWidget(self.tables[self.name])
        self.windows[self.name].statusBar()
        self.windows[self.name].resizeEvent = self.resizeEvent
        self.setupHexView()

    def setupQtWidgetConfigTab(self, **params):
        self.layouts['memory_config'].addWidget(self.groups['config'])
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
        # File branch
        self.trees['file'] = QtWidgets.QTreeWidgetItem(self.trees['config'], ['File'])
        self.trees['filename'] = QtWidgets.QTreeWidgetItem(self.trees['file'],
                                                           ['Filename', '', str(self.parent.filename)])
        self.buttons['filename'] = QtWidgets.QPushButton('Select')
        self.trees['config'].setItemWidget(self.trees['filename'], 1, self.buttons['filename'])
        # TODO: FIX SINGALLING CODE
        # self.buttons['filename'].connect(
        #	self.buttons['filename'],QtCore.SIGNAL('clicked()'),self.fileSelect)

        self.trees['fileNew'] = QtWidgets.QTreeWidgetItem(self.trees['file'],
                                                          ['Create', '', 'Create new file with selected name.'])
        self.buttons['fileNew'] = QtWidgets.QPushButton('New')
        self.trees['config'].setItemWidget(self.trees['fileNew'], 1, self.buttons['fileNew'])
        # TODO: FIX SIGNALLING CODE
        # self.buttons['fileNew'].connect(
        #	self.buttons['fileNew'],QtCore.SIGNAL('clicked()'),self.fileNew)

        self.trees['fileLoad'] = QtWidgets.QTreeWidgetItem(self.trees['file'],
                                                           ['Load', '', 'Load selected file.'])
        self.buttons['fileLoad'] = QtWidgets.QPushButton('Load')
        self.trees['config'].setItemWidget(self.trees['fileLoad'], 1, self.buttons['fileLoad'])
        # TODO: FIX SIGNALLING CODE
        # self.buttons['fileLoad'].connect(
        #	self.buttons['fileLoad'],QtCore.SIGNAL('clicked()'),self.fileOpen)

        self.trees['fileSave'] = QtWidgets.QTreeWidgetItem(self.trees['file'],
                                                           ['Save', '', 'Save selected file.'])
        self.buttons['fileSave'] = QtWidgets.QPushButton('Save')
        self.trees['config'].setItemWidget(self.trees['fileSave'], 1, self.buttons['fileSave'])
        # TODO: FIX SIGNALLING CODE
        # self.buttons['fileSave'].connect(
        #	self.buttons['fileSave'],QtCore.SIGNAL('clicked()'),self.fileSave)

        self.trees['config'].expandAll()

    def test(self):
        self.iCeDeROM.modules['gui'].dialogs['message'].information(
            self, 'Memory', 'This is a Memory Menu Test...')

    def setupHexView(self):
        '''Setup HexView header and table parameters.'''
        self.windowContentWidth = self.addrColumnWidth + self.asciiColumnWidth
        self.hexColumnMultiply = self.windows[self.name].width()
        self.hexColumnMultiply /= self.hexColumnWidth * self.hexColumnCount + self.addrColumnWidth
        self.window.setMinimumSize(self.windowContentWidthSingle, 100)
        self.tables[self.name].setColumnCount(self.hexColumnCount * self.hexColumnMultiply + 2)
        tableLabel = ['ADDRESS']
        # TODO: FIX FORMATTING PROBLEM
        # for i in range(0,self.hexColumnCount*self.hexColumnMultiply): tableLabel.append("%02X"%i)
        tableLabel.append('ASCII')
        self.tables[self.name].setHorizontalHeaderLabels(tableLabel)
        # TODO: FIX COMPONENT PROBLEM
        # self.tables[self.name].horizontalHeader().setResizeMode(QtWidgets.QHeaderView.Fixed)
        # TODO: FIX FORMATTING PROBLEM
        # for i in range(1,self.hexColumnCount*self.hexColumnMultiply+1):
        #	self.tables[self.name].setColumnWidth(i,self.hexColumnWidth)
        self.tables[self.name].setColumnWidth(0, self.addrColumnWidth)
        self.tables[self.name].setColumnWidth(self.hexColumnCount * self.hexColumnMultiply + 1, self.asciiColumnWidth)
        self.tables[self.name].setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def resizeEvent(self, QResizeEvent):
        '''Adjust HexView according to QtWidget/Window (re)size.'''
        size = QResizeEvent.size()
        width = size.width()
        height = size.height()
        self.setupHexView()

    def update(self):
        '''
			Update the HexView data with the one provided in parent's buffer.
			TODO: Chunk based preload depending on the scrollbar size.
		'''
        # if self.parent.filename==None: return
        self.parent.buffer.seek(0, io.SEEK_SET)
        cols = self.hexColumnCount * self.hexColumnMultiply
        rows = self.parent.size / (self.parent.chunksize / cols)
        if rows == 0: rows = 1
        chunk = 0
        print('ROWS: ' + str(rows))
        self.tables[self.name].setRowCount(rows)
        self.parent.chunkdata = self.parent.buffer.read(self.parent.chunksize)
        while self.parent.chunkdata:
            for column in range(0, cols):
                for row in range(0, rows):
                    byte = self.parent.chunkdata[column + row]
                    self.tables[self.name].setCurrentCell((chunk * rows) + row, column)
                    self.tables[self.name].setCurrentItem(QtWidgets.QTableWidgetItem("%02X" % byte))
            self.parent.chunkdata = self.parent.buffer.read(self.parent.chunksize)

    def fileNew(self):
        filename = self.iCeDeROM.modules['gui'].dialogs['file'].getSaveFileName(
            self.iCeDeROM.modules['gui'].window, 'New File')
        if filename == '': return
        self.parent.fileOpen(filename)
        self.update

    def fileOpen(self):
        filename = self.iCeDeROM.modules['gui'].dialogs['file'].getOpenFileName(
            self.iCeDeROM.modules['gui'].window, 'Open File')
        filename = str(filename)
        if filename == '': return
        self.parent.fileOpen(filename)
        self.update

    def fileSave(self):
        filename = self.iCeDeROM.modules['gui'].dialogs['file'].getSaveFileName(
            self.iCeDeROM.modules['gui'].window, 'Save File')
        if filename == '': return
        self.parent.fileSave(filename)
        self.update

    def fileSelect(self):
        filename = self.iCeDeROM.modules['gui'].dialogs['file'].getOpenFileName(
            self.iCeDeROM.modules['gui'].window, 'Select File')
        if filename == '': return
        self.parent.filename = str(filename)
        self.trees['filename'].setText(2, self.parent.filename)

    def bufferInit(self):
        return

    def bufferResize(self):
        return
