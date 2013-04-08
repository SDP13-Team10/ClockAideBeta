#!/usr/bin/python

# ClockAide System

import time, sys, random, sqlite3, string, usb, serial

#----------------------------------
# Database initialization
db = sqlite3.connect("./Database/ClockAideDB")
cursor = db.cursor()


#----------------------------------
# Keypad detection
keypad = serial.Serial()

#---------------------------------
#Normal Mode
greeting = "Welcome to ClockAide!"
mode = "Normal Mode"

def normal():
 print greeting
 print mode
 clock = time.ctime()
 print clock
 control = int(raw_input("Key pressed: "))
 if control == 0:
  modeSelect()
 elif control == 3:
  quit()

#----------------------------------
# Mode Selector
greeting = "Welcome to Quiz Mode."
menu = "Would you like to Read the time (1), or Set the time (2)?"
prompt = "User Selection:"
#u_input = input("User Selection: ")
m_read = 1
s_read = 2

def modeSelect():
 print greeting
 print menu
 u_input = int(raw_input("User Selection: ")) #Cast required
# print u_input

 if u_input == 1:
  read()
 elif u_input == 2:
  Set()
#----------------------------------
# Read Mode

def read():
 h = random.randrange(1,12)	
 m = random.randrange(0,59)
 attempt = 0
 correct = 0
 print "*************************"
 print 'Welcome to Read Mode.'
 print "*************************"
 r_prompt = 'What time is it?'

 sql = "SELECT * FROM students WHERE id=?"
 user = cursor.execute(sql, [("1")])
 start = time.ctime()				# Retrieve current time
 mode = 'Read'

# Move stepper motors here
 print r_prompt
 print h, m	# For debugging purposes only
 u_hr = int(raw_input("Hour: "))
 u_min = int(raw_input("Minute :"))

# Student response processing
 "%02d:%02d" % (u_hr, u_min)
 res_hr = str(u_hr)
 res_min = str(u_min)
 answer = res_hr+res_min

# Correct Answer ************** #
 if u_hr == h and u_min == m:
  print 'Correct! Good Job!'
  correct += 1

  sql = "INSERT INTO studentResponses (sid,studentResponse) VALUES (?,?)"
  cursor.execute(sql, [(correct), (answer)])
  db.commit()

  control = int(raw_input('Try again? 1 Yes 2 No '))
  if control == 1:
   read()
  elif control == 2:
   stopTime = time.ctime()			# Marks end of session
   print 'Thanks for playing.'
   print 'Saving activity data...'
# Record activity to database
   sql = "INSERT INTO sessionLog (sessionStartTime, sessionEndTime, type) VALUES (?,?,?)"
   cursor.execute(sql, [(start), (stopTime), (mode)]) # Need to figure out how to pull current user's ID (FK)
   db.commit()

   print 'Returning to normal mode...'
   normal()


# Wrong Answer **************** #
 else:
  print "*************************"	
  print 'Sorry! That is not the correct time. Try again.'
  while attempt != 3:
  # print 'Wrong answer. Try it again'
   u_hr = int(raw_input("Hour: "))
   u_min = int(raw_input("Minute :"))
   if u_hr == h and u_min == m:
    print 'Correct! Good Job!'
    correct += 1
    control = int(raw_input('Try again? 1 Yes 2 No '))
    if control == 1:
     read()
    elif control == 2:
     print 'Thanks for playing. Goodbye!'
     print 'Returning to normal mode...'
     normal()			# Return to normal mode
   else:
    ++attempt
    print 'Correct answer is...'
    print h, m
    print '*************************'
    read() 
# Record activity to database


def Set():
 h = random.randrange(0,12)	
 m = random.randrange(0,59)

 print "*************************"
 print 'Welcome to Set Mode.'
 print "*************************"

 r_prompt = 'Set the clock to the following time:'
# Display value on LCD screen
 print h , m	
 print r_prompt
 u_hr = int(raw_input("Hour: "))
 u_min = int(raw_input("Minute :"))
 print 'Done'



def main():
 normal()
# modeSelect()

main()
