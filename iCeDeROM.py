#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import sys
import git
import modules.ui.qt.main

class iCeDeROM(object):
	"""iCeDeROM main class."""
	def __init__(self, **params):
		"""
		Parameters:
			ui='qt' to enable QT UI (default).
		"""
		#GIT related stuff
		self.gitrepo=git.Repo()
		self.release='git-'+str(self.gitrepo.active_branch)+'-'
		self.release+=str(self.gitrepo.commit().hexsha)
		print 'iCeDeROM '+self.release+' initializing...'
		#Modules related stuff
		self.modules=dict() 
		if not params.has_key('ui'):
			print 'Default UI is QT..'
			params['ui']='qt'
		self.modules['ui']=modules.ui.qt.main.MainWindow(self)
		self.modules['ui'].start(self)

if __name__ == '__main__':
	iCD=iCeDeROM(ui='qt')

