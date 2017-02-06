#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'python_qt' (provides QtWidget for modules.cli.python iCeDeROM module.
# (C) 2014-2017 CeDeROM Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

from PyQt5 import QtCore, QtWidgets


class module(object):
    """
	Provides Qt Widget for modules.cli.python iCeDeROM module.
	"""

    def __init__(self, **params):
        """Create Qt Widget for Python CLI."""
        self.name = 'python_qt'
        if not 'iCeDeROM' in params:
            raise KeyError('iCeDeROM parameter reference mandatory!')
        if not 'gui' in params['iCeDeROM'].modules:
            raise RuntimeError('Python Console QtWidget requires GUI running!')
        self.iCeDeROM = params['iCeDeROM']
        self.tabs = dict()
        self.texts = dict()
        self.layouts = dict()
        self.window = None
        self.command = None
        self.history_index = 0
        self.history = list()
        self.createQtWidget(**params)
        self.setupQtWidget(**params)

    def setup(self, **params):
        """Setup the QtWidget."""
        return

    def start(self, **params):
        """Start the QtWidget."""
        try:
            self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(False)
            self.tabs['id'] = self.iCeDeROM.modules['gui'].tabs['system'].addTab(
                self.tabs[self.name], 'python')
            self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(True)
        except:
            self.iCeDeROM.modules['log'].log.exception('Cannot start ' + self.name + ' module!')

    def stop(self, **params):
        """Stop the QtWidget."""
        try:
            self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(False)
            self.iCeDeROM.modules['gui'].tabs['system'].removeTab(self.tabs['id'])
            self.iCeDeROM.modules['gui'].tabs['system'].setUpdatesEnabled(True)
        except:
            self.iCeDeROM.modules['log'].log.exception('Cannot start ' + self.name + ' module!')

    def createQtWidget(self, **params):
        """Create the QtWidget."""
        self.tabs[self.name] = QtWidgets.QTabWidget()
        self.window = self.tabs[self.name]
        self.layouts[self.name] = QtWidgets.QVBoxLayout(self.tabs[self.name])
        self.texts[self.name] = QtWidgets.QTextEdit()

    def setupQtWidget(self, **params):
        """Setup the QtWidget internals."""
        self.layouts[self.name].addWidget(self.texts[self.name])
        self.texts[self.name].setAcceptRichText(False)
        self.texts[self.name].setReadOnly(False)
        self.texts[self.name].setFontFamily("Courier")
        self.texts[self.name].keyPressEventOrig = self.texts[self.name].keyPressEvent
        self.texts[self.name].keyPressEvent = self.keyPressEvent

    def keyPressEvent(self, QKeyEvent):
        """Extend the QTextEdit key press event, add routines, then call the original method."""
        # TODO: FIX MISSING CURSOR CODE
        pass
        # cursor=self.texts[self.name].textCursor()
        if QKeyEvent.key() == QtCore.Qt.Key_Return:
            # Handle Return key -> execute python command
            # cursor.select(QtWidgets.QTextCursor.LineUnderCursor)
            self.texts[self.name].moveCursor(QtWidgets.QTextCursor.End, QtWidgets.QTextCursor.MoveAnchor)
            self.texts[self.name].setTextCursor(cursor)
            self.command = unicode(self.texts[self.name].textCursor().selectedText())
            self.texts[self.name].moveCursor(QtWidgets.QTextCursor.End, QtWidgets.QTextCursor.MoveAnchor)
            self.texts[self.name].insertPlainText('\n')
            self.texts[self.name].moveCursor(QtWidgets.QTextCursor.End, QtWidgets.QTextCursor.MoveAnchor)
            self.historyAppend(self.command)
            self.execute(self.command)
        elif QKeyEvent.key() == QtCore.Qt.Key_Up:
            # Display history item
            if self.history_index > 0: self.history_index -= 1
            cursor.select(QtWidgets.QTextCursor.LineUnderCursor)
            self.texts[self.name].setTextCursor(cursor)
            self.texts[self.name].insertPlainText(self.history[self.history_index])
            # Highlight last history item
            if self.history_index == len(self.history) - 1:
                cursor.select(QtWidgets.QTextCursor.LineUnderCursor)
                self.texts[self.name].setTextCursor(cursor)
        elif QKeyEvent.key() == QtCore.Qt.Key_Down:
            # Display history item
            if self.history_index < len(self.history) - 1:
                self.history_index += 1
            else:
                self.history_index = len(self.history) - 1
            cursor.select(QtWidgets.QTextCursor.LineUnderCursor)
            self.texts[self.name].setTextCursor(cursor)
            self.texts[self.name].insertPlainText(self.history[self.history_index])
            # Highlight last history item
            if self.history_index == len(self.history) - 1:
                cursor.select(QtWidgets.QTextCursor.LineUnderCursor)
                self.texts[self.name].setTextCursor(cursor)
        elif QKeyEvent.key() == QtCore.Qt.Key_PageUp:
            # Display history item
            self.history_index = 0
            cursor.select(QtWidgets.QTextCursor.LineUnderCursor)
            self.texts[self.name].setTextCursor(cursor)
            self.texts[self.name].insertPlainText(self.history[self.history_index])
        elif QKeyEvent.key() == QtCore.Qt.Key_PageDown:
            # Display history item
            self.history_index = len(self.history) - 1
            cursor.select(QtWidgets.QTextCursor.LineUnderCursor)
            self.texts[self.name].setTextCursor(cursor)
            self.texts[self.name].insertPlainText(self.history[self.history_index])
            # Highlight last history item
            if self.history_index == len(self.history) - 1:
                cursor.select(QtWidgets.QTextCursor.LineUnderCursor)
                self.texts[self.name].setTextCursor(cursor)
        else:
            # No more key extensions, call the original handler
            self.texts[self.name].keyPressEventOrig(QKeyEvent)

    def write(self, data):
        '''STDOUT write wrapper.'''
        # TODO: FIX MISSING CURSOR CODE
        return
        self.texts[self.name].insertPlainText(data)
        self.texts[self.name].moveCursor(QtWidgets.QTextCursor.End, QtWidgets.QTextCursor.MoveAnchor)

    def execute(self, command):
        """Super class should replace this with python evaluation routine."""
        raise Exception("CliPythonQt: No Python handler provided!")

    def historyAppend(self, command):
        """Append command to the history."""
        if command.strip() == '': return
        self.history.append(command)
        self.history_index = len(self.history)
