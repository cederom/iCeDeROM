#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# (C) 2014-2017 CeDeROM Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import sys,os
import git

class iCeDeROM(object):
	"""iCeDeROM main class."""
	def __init__(self, **params):
		"""
		Parameters:
			ui='qt'   to enable and start QT UI (default).
			ui='none' do not use UI.
		"""
		#Modules related stuff
		self.modules=dict()
		self.path=os.path.dirname(__file__)
		#Setup LOG module (mandatory)
		import iCeDeROM.log.log
		module=iCeDeROM.log.log.module(iCeDeROM=self)
		module.setup()
		self.modules[module.name]=module
		#GIT related stuff (mandatory)
		self.gitrepo=git.Repo()
		self.release='git-'+str(self.gitrepo.active_branch)+'-'
		self.release+=str(self.gitrepo.commit().hexsha)
		self.modules['log'].log.info('iCeDeROM %s init...', self.release)
		#Log Python details
		self.modules['log'].log.info('Using Python ('+sys.platform+') '+sys.version.replace('\n',''))
		#Setup GUI related modules (optional)
		self.ui=params['ui'] if 'ui' in params else 'qt'
		if self.ui=='qt':
			#Create the GUI MainWindow
			import iCeDeROM.ui.qt.QtMainWindow
			module=iCeDeROM.ui.qt.QtMainWindow.module(iCeDeROM=self, argv=sys.argv)
			self.modules['log'].log.info('Loading '+module.name+' ('+module.description+') module...')
			module.setup(iCeDeROM=self)
			self.modules[module.name]=module			
			#Load example mdiWindow module
			import iCeDeROM.ui.qt.QtMdiChildExample
			module=iCeDeROM.ui.qt.QtMdiChildExample.module(iCeDeROM=self)
			self.modules['log'].log.info('Loading '+module.name+' module...')
			module.setup(iCeDeROM=self)
			module.start(iCeDeROM=self)
			self.modules[module.name]=module
			#Load Python Console module
			import iCeDeROM.cli.python
			module=iCeDeROM.cli.python.module(iCeDeROM=self)
			self.modules['log'].log.info('Loading '+module.name+' module...')
			module.setup(iCeDeROM=self)
			module.start(iCeDeROM=self)
			self.modules[module.name]=module
		#Load the Memory Buffer module
		import iCeDeROM.memory.memory
		module=iCeDeROM.memory.memory.module(iCeDeROM=self)
		self.modules['log'].log.info('Loading '+module.name+' module...')
		module.setup(iCeDeROM=self)
		module.start(iCeDeROM=self)
		self.modules[module.name]=module
		#Load Interface Drivers Module
		import iCeDeROM.interface.interface
		module=iCeDeROM.interface.interface.module(iCeDeROM=self)
		self.modules['log'].log.info('Loading '+module.name+' module...')				
		self.modules[module.name]=module		
		module.setup(iCeDeROM=self)
		module.start(iCeDeROM=self)
		#Load the Terminal Module
		import iCeDeROM.cli.terminal
		module=iCeDeROM.cli.terminal.module(iCeDeROM=self)
		self.modules['log'].log.info('Loading '+module.name+' module...')				
		self.modules[module.name]=module		
		module.setup(iCeDeROM=self)
		module.start(iCeDeROM=self)		
		#When all is set start the UI
		if 'gui' in self.modules:
			self.retval=self.modules['gui'].start()
		self.modules['log'].log.info('iCeDeROM %s shutdown...', self.release)
		self.modules['log'].stop()

if __name__ == '__main__':
	iCD=iCeDeROM(ui='qt')
