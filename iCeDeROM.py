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
		#GIT related stuff
		self.gitrepo=git.Repo()
		self.release='git-'+str(self.gitrepo.active_branch)+'-'
		self.release+=str(self.gitrepo.commit().hexsha)
		print 'iCeDeROM '+self.release+' initializing...'
		#Modules related stuff
		self.modules=dict() 
		if not params.has_key('ui'): params['ui']='qt'
		if params['ui']=='qt':
			#Create the GUI MainWindow
			import modules.ui.qt.mainWindow
			module=modules.ui.qt.mainWindow.module(iCeDeROM=self, argv=sys.argv)
			module.setup(iCeDeROM=self)
			self.modules[module.name]=module
			#Import example mdiWindow
			import modules.ui.qt.mdiChild_example
			module=modules.ui.qt.mdiChild_example.module(iCeDeROM=self)
			module.setup(iCeDeROM=self)
			module.start(iCeDeROM=self)
			self.modules[module.name]=module
			#When all is set start the GUI
			self.modules['gui'].start()

if __name__ == '__main__':
	iCD=iCeDeROM(ui='qt')

