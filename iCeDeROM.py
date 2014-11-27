#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

#TODO: Use logger module to log events.

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
		self.modules['log'].log.info('iCeDeROM %s initializing...', self.release)		
		#Setup GUI related modules (optional)
		if not params.has_key('ui'): params['ui']='qt'
		if params['ui']=='qt':
			#Create the GUI MainWindow
			import modules.ui.qt.mainWindow
			module=modules.ui.qt.mainWindow.module(iCeDeROM=self, argv=sys.argv)
			module.setup(iCeDeROM=self)
			self.modules[module.name]=module
			self.modules['log'].log.info('Added module: %s', module.name)
			#Import example mdiWindow
			import modules.ui.qt.mdiChild_example
			module=modules.ui.qt.mdiChild_example.module(iCeDeROM=self)
			module.setup(iCeDeROM=self)
			module.start(iCeDeROM=self)
			self.modules[module.name]=module
			self.modules['log'].log.info('Added module: %s', module.name)
			#When all is set start the GUI
			self.modules['gui'].start()

if __name__ == '__main__':
	iCD=iCeDeROM(ui='qt')

