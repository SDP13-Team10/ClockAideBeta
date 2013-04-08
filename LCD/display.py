#!/usr/bin/env python

# LCD display

import serial, time, sys
SERIALPORT = "/dev/ttyAMA0"

def textBanner(word, s):
 cursor = 0
 for letter in word:
  s.write(letter)
  cursor = cursor + 1
  time.sleep(0.2) # set this delay to a comfortable value

def main():

 s = serial.Serial("/dev/ttyAMA0", 9600)
 time.sleep(2)
 s.write('\xFE\x01') # clear the LCD screen
 print "Clearing Screen..."
 while(True):
        time.sleep(1)
        s.write('\xFE\x80') # goto 0 position
	print "Setting cursor to start position..."
        #textstring = "1111111111111111222222222222222233333333333333334444444444444444"
        textstring = "ClockAide "
        #scrollText(textstring,s) # choose one of these
	print "Displaying text..."
        textBanner(textstring,s) # two options
        time.sleep(2)
        s.write('\xFE\x01') # clear the screen (in preparation to repeat)
 	print "Screen Cleared"

if __name__ == '__main__':
    main()
main()