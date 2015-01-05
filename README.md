<h1>iCeDeROM</h1>

(= In-Circuit Evaluate Debug and Edit for Research on Microelectronics =)

<h2>About</h2>
iCeDeROM - a Swiss Army Knife Multi-Tool for Digital Electronics - is a platform and hardware independent python-based low-level development and analysis software utility to work with microelectronic devices such as embedded and computer systems.

iCeDeROM was started by Tomasz Bolesław CEDRO (http://www.tomek.cedro.info) in 2014 as an Open-Source project.


<h2>Features</h2>

<h3>Available Features</h3>
<ul>
<li>Qt4 GUI: MDI (Multiple Document Interface) for modules windows, Panels for configuration, etc.</li>
<li>Logging: loglevels, file output, QtWidget output.</li>
<li>Python Console: buil-it python interpreter with access to all modules, QtWidget CLI.</li>
<li>Interface: various hardware interface infrastructure, QtWidget configuration.</li>
<li>Terminal: Serial Console Port terminal, QtWidget CLI.</li>
</ul>

<h3>Planned Features</h3>
<ul>
<li>Common iCeDeROM API.</li>
<li>No GUI operaitons (i.e. shell only).</li>
<li>Python scripts automation.</li>
<li>Interface Bitbang.</li>
<li>Transport Layer between Target Device and Interface Layer.</li>
<li>Various Hardware Interfaces support.</li>
<li>Memory buffer, chunk-based.</li>
<li>Hex Editor.</li>
<li>JTAG Support.</li>
<li>SWD Support.</li>
<li>MIPS CPU Support.</li>
<li>ARM CPU Support.</li>
<li>Intel CPU Support.</li>
<li>Debugging.</li>
<li>Memory Analysis.</li>
</ul>

<h2>Requirements, Dependencies, Hardware</h2>

<h3> Software Dependencies</h3>
<ul>
<li>Python 2.7</li>
<li>PyQt4</li>
<li>GitPython (download with pip)</li>
<li>pyLibFTDI (download with pip)
</ul>

<h3>Supported Hardware</h3>
<ul>
<li>FTDI USB Dongles - using LibFTDI wrapper</li>
<ul>
<li>Serial Console Port</li>
<li>Manual and Preset Configuration (presets available for
<a href="http://shop.kristech.pl/p/24/257/kt-link-.html" target="_blank">KT-LINK</a>
)
</ul>
</ul>


<h2>Developer's Scratchpad</h2>

iCeDeROM is supposed to work as standalone application, but it should be also possible to include it as Python module into external application. As for now all efforts are put into core functionalities, API clarification and Qt4 GUI. In future standalone operations in console and/or scripted invocation should be possible..

Modular design makes it possible to add new functionalities easily by use of existing software components that provide Python bindings. It should be also possible to interact with binaries and libraries that have no Python bindings. External modules and applications should be wrapped and adapted to work with iCeDeROM. Yet, no stable API is established. Below a functional proposition is presented.

modules/example/example.py:
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

modules/example/example_qt.py:
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

<small>iCeDeROM (C) 2014-2015 Tomasz Bolesław CEDRO, All rights reserved :-)</small> <a href="http://www.icederom.com">http://www.iCeDeROM.com</a>
