#!/usr/bin/env python

""" 
LCD test with a direct connection to serial port
4/3/13 Displays hello world correctly, but not the user input
"""

import serial, sys, time

s = serial.Serial(port = '/dev/ttyAMA0', baudrate = 9600)

while True:
 time.sleep(0.25)
 if s.isOpen():
	s.write(chr(12))	# Clear
	s.write("Hello")
	s.write(chr(13))	# New line
	s.write("world!")
#	s.write('Test')
# prompt = raw_input("Text: ")
