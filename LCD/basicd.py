#!/usr/bin/env python

""" 
LCD test with a direct connection to serial port
4/3/13 Displays hello world correctly, but not the user input
4/4/13 Testing static display. Works
"""

import serial, sys, time

s = serial.Serial(port = '/dev/ttyAMA0', baudrate = 9600)

#while True:
 #time.sleep(0.25)
#### Static Diplay
if s.isOpen():
	s.write(chr(12))	# Clear
	s.write("Hello")
	s.write(chr(13))	# New line
	s.write("world!")	# Stays on first line
#	s.write('Test')


while True:
 time.sleep(0.25)

 if s.isOpen():
    s.write(chr(12))
    s.write('\xFE\x80')
    s.write(chr(13))
    s.write("ClockAide")
    s.write("      Press any key")
    prompt = raw_input("Press any key: ")
    
 if prompt == 0:
     break
   
  

