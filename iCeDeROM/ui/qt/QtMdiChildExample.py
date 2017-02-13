#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'QtMdiChildExample' (example of iCeDeROM Module with mdiChildWindow QtWidget).
# (C) 2014-2017 CeDeROM Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import os
from PyQt5 import Qt, QtCore, QtWidgets, uic

uifilename = 'QtMdiChildExample.ui'


class module(object):
    """Example Module with Qt mdiChild window."""

    def __init__(self, **params):
        """
        Create Module and QtWidget.
        Parameters:
            iCeDeROM module reference (mandatory).
        """
        self.name = 'QtMdiChildExampleModule'
        if not 'iCeDeROM' in params:
            raise KeyError('iCeDeROM parameter reference mandatory!')
        if params['iCeDeROM'].ui != 'qt':
            raise RuntimeError('Interface QtWidget requires Qt GUI running!')
        self.iCeDeROM = params['iCeDeROM']
        self.ui = dict()
        if self.iCeDeROM.ui == 'qt':
            self.ui['qt'] = QtWidget(**params)

    def setup(self, **params):
        self.ui['qt'].setup(**params)

    def start(self, **params):
        self.ui['qt'].start(**params)

    def stop(self, **params):
        self.ui['qt'].stop(**params)


class QtWidget(QtWidgets.QMainWindow):
    """Example Module, Qt mdiChildWindow."""

    def __init__(self, **params):
        """
        Create window and add it to the iCeDeROM GUI.
        Parameters:
            iCeDeROM module reference (mandatory).
        """
        self.name = 'QtMdiChildExampleWindow'
        if not 'iCeDeROM' in params:
            raise KeyError('iCeDeROM parameter reference mandatory!')
        self.iCeDeROM = params['iCeDeROM']
        super(QtWidget, self).__init__()
        self.uifile = os.path.join(os.path.dirname(os.path.relpath(__file__))) + '/' + uifilename
        self.window = uic.loadUi(self.uifile, self)
        try:
            self.iCeDeROM.modules['gui'].mdi.addSubWindow(self.window)
        except:
            self.iCeDeROM.modules['log'].log.critical('Cannot addSubWindow!')
            raise
        self.window.setWindowTitle('QtMdiChildExample')
        self.window.pushButton.clicked.connect(lambda: self.listModules(**params))
        self.window.pushButton_2.clicked.connect(lambda: self.logMessage(**params))

    def setup(self, **params):
        return

    def start(self, **params):
        self.window.show()

    def stop(self, **params):
        self.window.hide()

    def listModules(self, **params):
        self.window.textBrowser.clear()
        self.window.textBrowser.append('Available Modules:')
        for module in self.iCeDeROM.modules:
            self.window.textBrowser.append(module)

    def logMessage(self, **params):
        self.iCeDeROM.modules['log'].log.info(self.window.logInput.toPlainText())
        self.window.logInput.clear()
