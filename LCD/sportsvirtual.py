#!/usr/bin/env python
#Scans virtual ports in Linux

import serial, glob

def scan():
 # Scans for available ports. Returns a list of device names
 return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*')

print "Found Ports"

for name in scan(): print name
