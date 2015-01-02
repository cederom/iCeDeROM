#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import sys
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
		#Setup LOG module (mandatory)
		import modules.log.log
		module=modules.log.log.module()
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
		self.ui=params['ui'] if params.has_key('ui') else 'qt'
		if self.ui=='qt':
			#Create the GUI MainWindow
			import modules.ui.qt.QtMainWindow
			module=modules.ui.qt.QtMainWindow.module(iCeDeROM=self, argv=sys.argv)
			self.modules['log'].log.info('Loading '+module.name+' module...')
			module.setup(iCeDeROM=self)
			self.modules[module.name]=module
			#Load example mdiWindow module
			import modules.ui.qt.QtMdiChildExample
			module=modules.ui.qt.QtMdiChildExample.module(iCeDeROM=self)
			self.modules['log'].log.info('Loading '+module.name+' module...')
			module.setup(iCeDeROM=self)
			module.start(iCeDeROM=self)
			self.modules[module.name]=module
			#Load Python Console module
			import modules.cli.python
			module=modules.cli.python.module(iCeDeROM=self)
			self.modules['log'].log.info('Loading '+module.name+' module...')
			module.setup(iCeDeROM=self)
			module.start(iCeDeROM=self)
			self.modules[module.name]=module
		#Load Interface Drivers Module
		import modules.interface.interface
		module=modules.interface.interface.module(iCeDeROM=self)
		self.modules['log'].log.info('Loading '+module.name+' module...')				
		self.modules[module.name]=module		
		module.setup(iCeDeROM=self)
		module.start(iCeDeROM=self)
		#Load the Terminal Module
		import modules.cli.terminal
		module=modules.cli.terminal.module(iCeDeROM=self)
		self.modules['log'].log.info('Loading '+module.name+' module...')				
		self.modules[module.name]=module		
		module.setup(iCeDeROM=self)
		module.start(iCeDeROM=self)		
		#When all is set start the UI
		if self.modules.has_key('gui'):
			self.retval=self.modules['gui'].start()
		self.modules['log'].log.info('iCeDeROM %s shutdown...', self.release)
		self.modules['log'].stop()


if __name__ == '__main__':
	iCD=iCeDeROM(ui='qt')

