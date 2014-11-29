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
		#Setup GUI related modules (optional)
		self.ui=params['ui'] if params.has_key('ui') else 'qt'
		if self.ui=='qt':
			#Create the GUI MainWindow
			import modules.ui.qt.QtMainWindow
			module=modules.ui.qt.QtMainWindow.module(iCeDeROM=self, argv=sys.argv)
			module.setup(iCeDeROM=self)
			self.modules[module.name]=module
			#Import example mdiWindow
			import modules.ui.qt.QtMdiChildExample
			module=modules.ui.qt.QtMdiChildExample.module(iCeDeROM=self)
			module.setup(iCeDeROM=self)
			module.start(iCeDeROM=self)
			self.modules[module.name]=module
			#Log available modules
			modlist=str('Loaded modules:')
			for module in self.modules.keys(): modlist+=' '+module
			self.modules['log'].log.info(modlist)
			#When all is set start the GUI
			self.retval=self.modules['gui'].start()
			self.modules['log'].log.info('iCeDeROM %s shutdown...', self.release)
			self.modules['log'].stop()

if __name__ == '__main__':
	iCD=iCeDeROM(ui='qt')

