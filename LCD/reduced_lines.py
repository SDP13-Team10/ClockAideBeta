
#!/usr/bin/env python
# encoding: utf-8
"""
TweetLCD.py
 
This twitter-to-LCD script implements two functions for displaying
text on a Sparkfun Serial LCD.
 
 scrollText - allows long lines of text to be scrolled along the top of the LCD
 pageText - allows long text to be paged up. First the top line is written, then
            the bottom line, then the lines shift up, and more text is
            written on the bottom line.
 
Created by Andrew M.C. Dawes on 2009-12-18.
Copyright (c) 2009 Andrew M.C. Dawes.
Some rights reserved. License: Creative Commons GNU GPL:
 
http://creativecommons.org/licenses/GPL/2.0/
 
"""
 
import serial, time, sys
SERIALPORT = "/dev/ttyAMA0" # this is my USB serial port YMMV

def lcdInitialize():
 while True:
  try:
	# Try to connect
	lcd = serial.Serial(SERIALPORT)
	return lcd
  except:
	# Connetion Failed
	print "No Connection"
	time.sleep(2)
 
def pageText(textstring, s):
    botline = ""
    cursor = 0
    for letter in textstring:
        # print letter, cursor   # this is for debugging
        s.write(letter)
 
        if cursor > 15:
            # I'm printing in second line so keep track of what I write
            botline = botline + letter
            # print botline
 
        if cursor == 31: # page the bottom line up to top, clear bottom, and write
            # print "cursor wrap"
            s.write('\xFE\x80') # wrap to start of first line
            s.write(botline) # write what was on the bottom (now on top)
            s.write("                ")
            s.write('\xFE\xC0') # skip to beginning of second line
            botline = ""
            cursor = 15 # reset to beginning of second line
 
        cursor = cursor + 1
 
        time.sleep(0.2) # set this delay to a comfortable value
 
def scrollText(textstring, s):
    nextstring = ""
    cursor = 0
    firstpass = True # test whether this is the first 16 characters
    for letter in textstring:
        if firstpass == False:
            s.write('\xFE\x18') # scroll left one spot at each letter
 
        # print letter, cursor  # this is for debugging
        s.write(letter)
 
        if cursor == 7:
            # I'm printing the last visible character
            s.write('\xFE\x90') # jump cursor to 2nd column of 16
            firstpass = False # once the first row is filled, we need to scroll
 
        if cursor == 15:
            s.write('\xFE\xA0') # jump cursor to 3rd column
 	    s.write(letter)
        if cursor == 20:
            cursor = -1 # start over, there are only 40 characters in memory
            s.write('\xFE\x80') # this is the original character address.
 
        cursor = cursor + 1
 
        #time.sleep(0.2) # adjust this to a comfortable value
 	time.sleep(0.5)
def main():
    s = serial.Serial("/dev/ttyAMA0", 9600)
    lcdInitialize()
    time.sleep(2)
    s.write('\xFE\x01') # clear the LCD screen
    print "Clearing Screen..."
    while(True):
        time.sleep(1)
        s.write('\xFE\x80') # goto 0 position
	print "Setting cursor to start position..."
        #api = twitter.Api()
 #       status = api.GetUserTimeline(user='DrDawes',count=1)[0]
        textstring = "1111111111111111222222222222222233333333333333334444444444444444"
        #textstring = "ClockAide "
        scrollText(textstring,s) # choose one of these
	print "Displaying text..."
       # pageText(textstring,s) # two options
        time.sleep(2)
        s.write('\xFE\x01') # clear the screen (in preparation to repeat)
 	print "Screen Cleared"










    s.close()
 
if __name__ == '__main__':
    main()
