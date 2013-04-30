# 4/30/13 Used to merge with ClockAide software to prepare LCD screen for use
#	  Does not stop after count value is reached

import serial, time, sys
SERIALPORT = "/dev/ttyAMA0" # this is my USB serial port YMMV
s = serial.Serial("/dev/ttyAMA0", 9600)

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
#    global s
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

def display():
 time.sleep(2)
 s.write('\xFE\x01') # clear the LCD screen
 print "Clearing Screen..."

 count = 0
 while(count < 5):
        time.sleep(1)
        s.write('\xFE\x80') # goto 0 position
	print "Setting cursor to start position..."
        
        textstring = "ClockAide       Initializing..."
        #scrollText(textstring,s) # choose one of these
	print "Displaying text..."
        pageText(textstring,s) # two options
        time.sleep(2)
        s.write('\xFE\x01') # clear the screen (in preparation to repeat)
 	print "Screen Cleared"
 	++count
 s.close()

def main():
 lcdInitialize()
 display() 
 
if __name__ == '__main__':
    main()