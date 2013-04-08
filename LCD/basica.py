#!/usr/bin/env python

"""
LCD Serial Communication Test
Currently takes user input and displays on screen instantly

"""

import serial, time, sys
SERIALPORT = "/dev/ttyAMA0" 	# Pin 2: GND Pin 4: 5V Pin 6: RX

def initialize():
 s = serial.Serial(SERIALPORT, 9600) 
 s.write('\xFE\x33')
 s.write('\xFE\x32')
 s.write('\xFE\x28')
 s.write('\xFE\x0C')
 s.write('\xFE\x06')
 s.write('\xFE\x01')

def main():
  initialize()	
  print "initializing...\n"
  #s = serial.Serial("/dev/ttyAMA0", 9600)	# Open serial port
  s = serial.Serial(SERIALPORT, 9600)  
  time.sleep(2)
  print "Ready\n"
  s.write('\xFE\x01') # clear the LCD screen
  print "Clearing Screen..."
  
  # Set up text display
  cursor = 0
  firstpass = True

  while(True): 
    #time.sleep(2)
    s.write('xFE\x80')  # Moving cursor to start position
    print "Moving cursor to start of line"

    text = "ClockAide"
    text2 = "1111111111111111222222222222222233333333333333334444444444444444"
    botline = text
    #greeting = raw_input("Text: ")

    for i in botline:
     #s.write('xFE\x02\x01')
     s.write('xFE\x02')
     s.write(botline)

     if cursor == 15:
      s.write('xFE\xC0')
     
     if cursor == 39:
	cursor = -1
	s.write('\xFE\x80')

     cursor = cursor + 1

print "End of test."
   

#s.close()		# close serial connection.
 
if __name__ == '__main__':	# This format is used to make the script global among all operating systems
    main()
