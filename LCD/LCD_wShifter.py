#!/usr/bin/python
#
# HD44780 LCD Test Script for
# Raspberry Pi
#
# Author : Rick Seiden (based on the work of Matt Hawkins)
# Site   : http://www.raspberrypi-spy.co.uk
# 
# Date   : 10/20/2012
#

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import
import RPi.GPIO as GPIO
import time
from datetime import datetime
from shifter import Shifter
# Define Shifter to LCD mapping
LCD_RS = 16 #Bin value
LCD_E  = 32 #Bin value
LCD_D4 = 1 
LCD_D5 = 2
LCD_D6 = 4
LCD_D7 = 8

# Define some device constants
LCD_WIDTH = 40    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def main():
  # Main program block

  shifter.clear()

  # Initialise display
  lcd_init()

  running=True
  while running==True:
    try:
	  lcd_byte(0x01, LCD_CMD)
      lcd_byte(LCD_LINE_1, LCD_CMD)
      lcd_string(datetime.now().strftime("%I:%M:%S %p"))
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(datetime.now().strftime("%A, %B %e, %Y"))
    except (KeyboardInterrupt):
      running=False

  lcd_byte(0x01,LCD_CMD)
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)  
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)  

def lcd_string(message):
  # Send string to display

  message = message.center(LCD_WIDTH," ")  

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  if (mode==True):
    value=LCD_RS
  else:
    value=0

  # High bits
  if bits&0x10==0x10:
    value=value+LCD_D4
  if bits&0x20==0x20:
    value=value+LCD_D5
  if bits&0x40==0x40:
    value=value+LCD_D6
  if bits&0x80==0x80:
    value=value+LCD_D7
  #print (value)
  # Toggle 'Enable' pin
  value=value+LCD_E
  time.sleep(E_DELAY)
  shifter.setValue(value)
  time.sleep(E_PULSE)
  shifter.clear()
  time.sleep(E_DELAY)      

  # Low bits
  if (mode==True):
    value=LCD_RS
  else:
    value=0
  if bits&0x01==0x01:
    value=value+LCD_D4
  if bits&0x02==0x02:
    value=value+LCD_D5
  if bits&0x04==0x04:
    value=value+LCD_D6
  if bits&0x08==0x08:
    value=value+LCD_D7

  # Toggle 'Enable' pin
  value=value+LCD_E
  time.sleep(E_DELAY)
  shifter.setValue(value)
  time.sleep(E_PULSE)
  shifter.clear()
  time.sleep(E_DELAY)

if __name__ == '__main__':
  GPIO.setmode(GPIO.BOARD)
  shifter=Shifter()
  main()

