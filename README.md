# iCeDeROM

**In-Circuit Evaluate Debug and Edit for Research on Microelectronics**

http://www.icederom.com

# About
iCeDeROM - a Swiss Army Knife Multi-Tool for Digital Electronics - is a platform and hardware independent python-based low-level development and analysis software utility to work with microelectronic devices such as embedded and computer systems.

iCeDeROM was started by CeDeROM Tomasz Bolesław CEDRO (http://www.tomek.cedro.info) in 2014 as an Open-Source project.


# Features

## Available Features / Work in Progress..

- [X] Python 3.6.
  - [X] Switch from Python 2.7 to Python 3.6.
  - [X] Run all from Virtualenv.
  - [ ] Make sure all functions work on Python3.6.
  - [ ] Automate Python+Virtualenv+Dependencies setup.
- [X] Qt5 GUI: MDI (Multiple Document Interface) for modules windows, Panels for configuration, etc.
  - [X] Switch from PyQt4 to PyQt5.
  - [ ] Make sure all functions work on PyQt5.
- [X] Logging: loglevels, file output, QtWidget output.
  - [ ] Fix broken logging after switch to PyQt5.
- [X] Python Console: buil-it python interpreter with access to all modules, QtWidget CLI.
  - [ ] Add prompt to built-int interpreter shell.
- [X] Interface: various hardware interface infrastructure, QtWidget configuration.
  - [ ] Make Terminal use Interface encoding.
- [X] Terminal
  - [x] Serial Console Port terminal
  - [X] QtWidget.
  - [ ] Terminal history search + highlight.
  - [ ] RegExp search + highlight.
  - [ ] Terminal cursor/move/select/append fixes.
  - [ ] Copy/Paste.
  - [ ] Disconnect.


## Planned Features

- [ ] Common iCeDeROM API.
- [ ] No GUI operaitons (i.e. shell only).
- [ ] Python scripts automation.
- [ ] Interface Bitbang.
- [ ] Transport Layer between Target Device and Interface Layer.
- [ ] Various Hardware Interfaces support.
- [ ] Memory buffer, chunk-based.
- [ ] Hex Editor + annotations.
- [ ] JTAG Support.
- [ ] SWD Support.
- [ ] MIPS CPU Support.
- [ ] ARM CPU Support.
- [ ] Intel CPU Support.
- [ ] Debugging.
- [ ] Memory Analysis.


# Requirements, Dependencies, Hardware

## Python Virtual Environment

A switch from Python2.7 to Python3.6 is almost complete. This helps
keeping all dependencies coherent and independent from underlying
operating system packages. See [Virtualenv](doc/virtualenv.md) manual
for more information.
* Python Virtualenv location is assumed to be `../venv/default/bin/python`
* `venv.sh` script will bring you inside virtualenv for testing.
* `iCeDeROM.sh` script will launch application using virtualenv.

## Software Dependencies
* Python 3.6.
* PyQt5.
* GitPython (download with pip)
* pyLibFTDI (download with pip)

A dedicated [requirements.txt](requirements.txt) file has been provided
that will help you install dependencies with `pip`:

```
pip install -r requirements.txt
```

## Supported Hardware

- [X] FTDI USB Dongles
  - [X] Use LibFTDI. No need to install device driver!
- [X] Serial Console Port
  - [X] LibFTDI based, no need to install device driver!
  - [X] Manual and Preset Configuration (presets available for <a href="http://shop.kristech.pl/p/24/257/kt-link-.html" target="_blank">KT-LINK</a>)


# Documentation

## Manuals

* [Virtualenv](doc/virtualenv.md): Python Virtual Environment Reference Manual.


## Developer's Scratchpad

iCeDeROM is supposed to work as standalone application, but it should be also possible to include it as Python module into external application. As for now all efforts are put into core functionalities, API clarification and Qt4 GUI. In future standalone operations in console and/or scripted invocation should be possible..

Modular design makes it possible to add new functionalities easily by use of existing software components that provide Python bindings. It should be also possible to interact with binaries and libraries that have no Python bindings. External modules and applications should be wrapped and adapted to work with iCeDeROM. Yet, no stable API is established. Below a functional proposition is presented.

Please note that below examples are just example of the organization. I am switching to Python3.6 and PyQt5 now..

Here is an example Core Module - a set of objects and functions wrapped in a Python Module:
```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# Here is the code for iCeDeROM Core Module.
# It provides essential functions and objects for the application.
# Other parts are provided in a separate file (i.e. QtWidget GUI).
# Core Module should work with no GUI, even as separate Python module.

class module(object):
	"""
	Example Module with QtWidget window.
	Each Core Module must have Setup,Start,Stop routines.
	Setup may be called multiple times to reconfigure the Module.
	"""
	def __init__(self, **params):
		"""
		Create Module and QtWidget if necessary.
		Parameters:
			iCeDeROM module reference (mandatory).
			parent   parent module reference.
		"""
		self.name='example'		
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		self.iCeDeROM=params['iCeDeROM']
		self.ui=dict()
		self.parent=params['parent'] if params.has_key('parent') else None
		if self.iCeDeROM.ui=='qt':
			import example_qt
			params['parent']=self
			self.ui['qt']=example_qt.module(**params)

	def setup(self,**params):
		"""Setup the module and submodules."""
		if self.iCeDeROM.ui=='qt':
			self.ui['qt'].setup(**params)
		#your setup code goes here

	def start(self, **params):
		"""Start the module and submodules."""
		if self.iCeDeROM.ui=='qt':
			self.ui['qt'].start(**params)
		#your startup code goes here

	def stop(self, **params):
		"""Stop the module and submodules."""
		if self.iCeDeROM.ui=='qt':
			self.ui['qt'].stop(**params)
		#your stop code goes here

	#you can define other methods for your module here
```

Here is an example of standalone Module that provides QtWidget GUI implemented with QtDesigner / UI creator:
```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# Here is the code for iCeDeROM Module GUI / QtWidget.
# It uses the UIC and QtDesigner UI creator.
# It provides only a GUI/QtWidget frontend for its parent Core Module.
# It should not perform any operations itself, just a frontend.
# Remember that operations should be performed by a Core Module, not here.

import os
from PyQt4 import Qt,QtCore,QtGui,uic

uifilename='QtMdiChildExample.ui'

class QtWidget(QtGui.QMainWindow):
	"""Example Module, Qt mdiChildWindow frontend."""
	def __init__(self, **params):
		"""
		Create window and add it to the iCeDeROM GUI.
		Parameters:
			iCeDeROM module reference (mandatory).
			parent   parent module reference.
		"""
		self.name='QtMdiChildExampleWindow'
		if not params.has_key('iCeDeROM'):
			raise KeyError('iCeDeROM parameter reference mandatory!')
		self.iCeDeROM=params['iCeDeROM']
		self.parent=params['parent'] if params.has_key('parent') else None
		super(QtMainWindow, self).__init__()
		self.uifile=os.path.join(
			os.path.dirname(os.path.relpath(__file__)))+'/'+uifilename
		self.window=uic.loadUi(self.uifile, self)
		try:
			self.iCeDeROM.modules['gui'].mdi.addSubWindow(self.window)
		except:
			self.iCeDeROM.modules['log'].log.critical('Cannot addSubWindow!')
			raise
		self.window.setWindowTitle('QtMdiChildExample')
		self.window.connect(self.window.pushButton,
			QtCore.SIGNAL('clicked()'), lambda:self.listModules(**params))
		self.window.connect(self.window.pushButton_2,
			QtCore.SIGNAL('clicked()'), lambda:self.logMessage(**params))

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
			
```

Here is an example of Module that provides QtWidget for a Terminal Core Module, but all Qt components are coded inside:
```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# Here is the code for iCeDeROM Terminal GUI / QtWidget.
# All Qt components are hardcoded here, no UI creator was used.

from PyQt4 import QtCore,QtGui

class module(QtGui.QWidget):
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
		super(module, self).__init__()
		self.parent=params['parent'] if params.has_key('parent') else None
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
		self.texts[self.name].moveCursor(
			QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
		
	def test(self):
		self.iCeDeROM.modules['gui'].dialogs['message'].information(
			self,'Terminal','This is a Terminal Menu Test...')
```

# References

## Articles and Publications
 1. Tomasz CEDRO, Marcin KUZIA, Antoni GRZANKA, ["LibSWD, Serial Wire Debug Open Framework for Low-Level Embedded Systems Access"](https://www.researchgate.net/publication/261079643_LibSWD_Serial_Wire_Debug_Open_Framework_for_Low-Level_Embedded_Systems_Access), Computer Science and Information Systems (FedCSIS), 2012 Federated Conference on, IEEE, 9-12 Sept. 2012, 615 - 620, E-ISBN 978-83-60810-51-4, Print ISBN 978-1-4673-0708-6. DOI: 10.13140/RG.2.1.1412.8722.
 2. Tomasz CEDRO, Marcin KUZIA, ["A Bits' Life"](https://www.researchgate.net/publication/269094704_A_Bits'_Life), Hakin9 Mobile Security, 2012/2, 34-40, 02/2012(3) ISSN: 1733-7186.
 3. Mordechai Guri, Yuri Poliak , Bracha Shapira, Yuval Elovici, ["JoKER: Trusted Detection of Kernel Rootkits in Android Devices via JTAG Interface"](http://arxiv.org/ftp/arxiv/papers/1512/1512.04116.pdf), Trustcom/BigDataSE/ISPA, 2015 IEEE  (Volume:1), 20-22 Aug. 2015, 65 - 73, INSPEC Accession Number: 15635781. DOI: 10.1109/Trustcom.2015.358.


*iCeDeROM (C) 2014-2017 CeDeROM, Tomasz Bolesław CEDRO (http://www.tomek.cedro.info), All rights reserved! :-)*

