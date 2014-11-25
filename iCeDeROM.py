#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# (C) 2014 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

import sys
import modules.ui.qt.main

class iCeDeROM(object):
	"""iCeDeROM main class."""
	def __init__(self):
		print 'iCeDeROM initializing...'
		self.modules=dict() 

if __name__ == '__main__':
	print 'Application loading...'
	iCD=iCeDeROM()
	iCD.modules['ui']=modules.ui.qt.main.MainWindow()
	iCD.modules['ui'].start()
