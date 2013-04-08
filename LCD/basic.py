#!/usr/bin/env python

"""
LCD Serial Communication Test

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
    botline = text2

# take each character from text, and put it on the screen
    for letter in text:
      
	if firstpass == False:
            #s.write('\xFE\x18') # scroll left one spot at each letter
	    s.write('\xFE\xC0')
        s.write(letter)

        
        
	
        #s.write(botline)
	cursor = cursor + 1


 #s.write(botline)
        print "Displaying text.....\n"
	time.sleep(2)

    #s.write('\xFE\x01') # clear the screen (in preparation to repeat)
    #print "Screen Cleared\n"

print "End of test."
   

#s.close()		# close serial connection.
 
if __name__ == '__main__':	# This format is used to make the script global among all operating systems
    main()