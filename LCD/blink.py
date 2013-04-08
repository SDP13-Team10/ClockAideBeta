#!/usr/bin/python
# Jean Yav
# projekrex@gmail.com
# Simple Diagram
#
# GPIO#7 >>>> RESISTOR(470ohm) >>>(+)LED >>> GND
#
from time import sleep
import RPi.GPIO as GPIO

# Pin configuration
LED= 7

# Pin setup
GPIO.setmode(GPIO.BCM)

# Led pin configured as ouput
GPIO.setup(LED, GPIO.OUT)

# control the delay (in sec)
delay = 2

run = True
state = True
while(run):

  try:

	GPIO.output(LED, state)
	state = not state
	sleep(delay)

  except KeyboardInterrupt:
	 run = False
	 GPIO.cleanup()
