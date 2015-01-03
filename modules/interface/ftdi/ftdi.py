#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
#
# iCeDeROM: In-Circuit Evaluate Debug and Edit for Research on Microelectronics
# Module 'ftdi.uart' (provides UART comms with FTDI based interfaces).
# (C) 2014-2015 Tomasz Bolesław CEDRO (http://www.tomek.cedro.info)
# All rights reserved, so far :-)

interfaces = {
 'Custom':{'vid':0x0000, 'pid':0x0000, 'uart_interface':''},
 'KT-LINK':{'vid':0x0403 ,'pid':0xbbe2, 'uart_interface':2}
}