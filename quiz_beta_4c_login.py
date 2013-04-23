#!/usr/bin/python

# Quiz Mode

import time
import sys
import random
import sqlite3
import string
import usb
import serial
import string


#ID_input

#----------------------------------
# Database initialization
db = sqlite3.connect("./Database/ClockAideDB")
cursor = db.cursor()


#----------------------------------
# Keypad detection
keypad = serial.Serial()

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
  sessionCount = 0
  sessionCount += 1
  sessionStart = time.ctime()
  
  #cursor.execute("INSERT INTO sessionLog VALUES ('ID = 2345','sessionCount', 'sessionStart','0', 'Read')")
  #db.commit()
  read()
 elif u_input == 2:
  sessionCount += 1
  sessionStart = clock.ctime()
  
  cursor.execute("INSERT INTO sessionLog VALUES ('ID', 'sessionCount', 'sessionStart','0', 'Set')")
  db.commit()
  Set()
 elif u_input == 0:
  #print 'Programming Mode'
  prog()
  quit()
#----------------------------------
# Read Mode

def read():
 h = random.randrange(1,12)	
 m = random.randrange(0,59)
 attempt = 0
 correct = 0
 sessionCount = 0
 sessionCount += 1

 print "*************************"
 print 'Welcome to Read Mode.'
 print "*************************"
 r_prompt = 'What time is it?'
 
 sql = "SELECT * FROM students WHERE id=?"
 user = cursor.execute(sql, [("1")])
 start = time.ctime()
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
   stopTime = time.ctime()
   print 'Thanks for playing.'
   print 'Saving activity data...'
   # Record activity to database
   sql = "INSERT INTO sessionLog (sessionStartTime, sessionEndTime, type) VALUES (?,?,?)"
   cursor.execute(sql, [(start), (stopTime), (mode)]) # Need to figure out how to pull current user's ID (FK)
   db.commit()

   #sql = "INSERT INTO sessionLog (sessionStartTime, sessionEndTime, type) VALUES (?,?,?)"
   #cursor.execute(sql, [(start), (stopTime), (mode)]) # Need to figure out how to pull current user's ID (FK)
   #db.commit()
   print 'Goodbye!'
   quit()		# Return to normal mode


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
     quit()			# Return to normal mode
   else:
    attempt += 1
    print 'Correct answer is...'
    print h, m
    print '*************************'
    read() 
# Record activity to database

#----------------------------------
# Set Mode
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

#----------------------------------
# Programming Mode
def prog():
 print '===================='
 print '||Programming Mode||'
 print '===================='
 print 'Enter lunch number'
 ID_input = int(raw_input("Lunch Number: ")) #Cast required
 name = raw_input("Name: ")

 
 sql = "INSERT INTO students (id, Name) VALUES (?,?)"
 cursor.execute(sql, [(ID_input), (name)])
 db.commit()

def insertSessionData(start, user, sessionEnd):
 sessionStart = time.ctime()
 user = cursor.execute("SELECT * FROM students WHERE ID = 1234")
 sessionEnd = 0
 mode = "Read"
 
def userLogin():
 user = int(raw_input("Enter your lunch number: "))
 
 sql = "SELECT id FROM students WHERE id=?"
 auth = cursor.execute(sql, [(user)])
 print auth
 data = cursor.fetchall()
 print data

 if user == auth:
  print 'User authenticated. Starting ClockAide....'
  current = user

 elif user != auth:
  print 'Invalid lunch number. Please try again....'

def userLogout():
  current = 0
 
def main():
 userLogin()
 modeSelect()

main()
