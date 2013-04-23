#!/usr/bin/python

# ClockAide System
# User Login, LCD display
# 4/6/13 Voice map, set mode, fixed time display
# 4/7/13 Fixed voice prompt in Set mode, Adjusted displays for both read and set

import time, datetime, sys, random, sqlite3, string, usb, serial, os, datetime, re

#---------------------------------
# Tracking system
id = 0
correct = 0
attempt = 0
sessionCount = 0
sessionStart = 0

#----------------------------------
# Database initialization
db = sqlite3.connect("./Database/ClockAideDB")
cursor = db.cursor()


#----------------------------------
# LCD Display
s = serial.Serial(port = '/dev/ttyAMA0', baudrate = 9600)
# x80 is the first spot on line 1
# x90 is the first spot on line 2


#----------------------------------
# Keypad detection (DEPRECATED 4/3/13)
keypad = serial.Serial()

#---------------------------------
#Normal Mode
greeting = "Welcome to ClockAide!"
mode = "Normal Mode"

def normal():
 global sessionCount

 if s.isOpen():
	s.write(chr(12))	# Clear
	s.write('\xFE\x01')	# This method works better to clear the line
	s.write(" Welcome!  < = >") # Spacing is exact!!!!!!!!
	s.write(chr(13))	# New line
	s.write("Normal Mode")	# Stays on first line

 print greeting
 print mode
 clock = time.ctime()
 hourNow = datetime.datetime.now().strftime("%I")
 minuteNow = datetime.datetime.now().strftime("%M")
 modulation = datetime.datetime.now().strftime("%p")
# print clock

 print hourNow, minuteNow, modulation
 speakTime(hourNow,minuteNow) 
 #speakTime(1,0) Debugging prompt in set mode
 time.sleep(2)
 s.write('\xFE\x01')
 s.write(clock)

 time.sleep(5)
 s.write('\xFE\x01')
 s.write('Quiz Mode? (1) Yes (2) No')
 control = int(raw_input("Key pressed: "))
 if control == 1:
  modeSelect()
 elif control == 2:
  quit()
"""  Testing
while True:
 print greeting
 print mode
 clock = time.ctime()
 print clock

 time.sleep(2)
 s.write('\xFE\x01')
 s.write(clock)
 switch = int(raw_input("(1) Quiz (2) Quit: ")
 time.sleep(5)

if switch == 1:
 s.write('\xFE\x01')
 s.write('Quiz Mode? (1) Yes (2) No')
 control = int(raw_input("Key pressed: "))
if control == 1:
  modeSelect()
elif control == 2:
  quit()
"""
#----------------------------------
# Mode Selector
greeting = "Welcome to Quiz Mode."
menu = "Would you like to Read the time (1), or Set the time (2)?"

prompt = "User Selection:"
#u_input = input("User Selection: ")
m_read = 1
s_read = 2

def modeSelect():
 #print greeting			# Computer display
 #print menu
 global id
 global sessionCount
 s.write('\xFE\x01')		# LCD Display
 s.write('Welcome to Quiz Mode')
 time.sleep(2)

 s.write('\xFE\x01')
 s.write('Read (1) Set (2)')
 u_input = int(raw_input("User Selection: ")) #Cast required

 
 
# print u_input
 
 if u_input == 1:
  s.write('\xFE\x01')
  s.write('New Read Session....')
  sessionCount = 0
  sessionCount += 1
  sessionStart = time.ctime()
  
  #cursor.execute("INSERT INTO sessionLog VALUES ('ID','sessionCount', 'sessionStart','0', 'Read')")
  #db.commit()
  read()
 elif u_input == 2:
  s.write('\xFE\x01')
  s.write('New Set Session....')
  sessionCount += 1
  sessionStart = time.ctime()
  
  s.write('\xFE\x01')
  s.write('New Set Session....')
  #cursor.execute("INSERT INTO sessionLog VALUES ('ID', 'sessionCount', 'sessionStart','0', 'Set')")
  #db.commit()
  Set()
 elif u_input == 0:
  #print 'Programming Mode'
  s.write('\xFE\x01')
  s.write('ID Programming Mode')
  prog()
  #quit()
#----------------------------------
# Read Mode

def read():
 global correct		# In python, this is required to tell the interpreter
 global attempt		# to use the definition at the top of the program
 global sessionCount
 global sessionStart

 h = random.randrange(1,12)	
 m = random.randrange(0,59)
 
 print "*************************"
 s.write('\xFE\x01')
 s.write('Read Mode')
 print 'Welcome to Read Mode.'
 print "*************************"
 
# Time display. Needs to be sent to LCD screen as a character. Source is an object
 hour = "%d" % h
 min = "%d" % m

 s.write('\xFE\x01')
 s.write('What time is it?')
 time.sleep(1)
 r_prompt = 'What time is it?'

 sql = "SELECT * FROM students WHERE id=?"
 user = cursor.execute(sql, [("1")])
 start = time.ctime()				# Retrieve current time
 mode = 'Read'

# Move stepper motors here
 print r_prompt

 s.write('\xFE\x01')
 print h, m	# For debugging purposes only
 s.write('\xFE\x91')
 s.write(hour)
 s.write('\xFE\x89')
 s.write(min)
 time.sleep (2)

 s.write('\xFE\x9D')
 s.write('Hour:')
 u_hr = int(raw_input("Hour: "))
 s.write('\xFE\x95')
 s.write('Minute:')
 u_min = int(raw_input("Minute :"))

 time.sleep(2)

# Student response processing
 "%02d:%02d" % (u_hr, u_min)
 res_hr = str(u_hr)
 res_min = str(u_min)
 answer = res_hr+res_min

# Correct Answer ************** #
 if u_hr == h and u_min == m:
  print 'Correct! Good Job!'
  s.write('\xFE\x01')
  s.write('Correct! Good Job!')
  time.sleep(1)

  correct += 1
  print correct

  sql = "INSERT INTO studentResponses (sid,studentResponse) VALUES (?,?)"
  cursor.execute(sql, [(correct), (answer)])
  db.commit()
  
  s.write('\xFE\x01')
  s.write('Try again? (1) Yes (2) No')
  control = int(raw_input('Try again? 1 Yes 2 No '))
  if control == 1:
   read()
  elif control == 2:
   stopTime = time.ctime()			# Marks end of session
 
   s.write('\xFE\x01')
   s.write('Thanks for      playing')
   time.sleep(1)

   print 'Thanks for playing.'
   time.sleep(1)
   s.write('\xFE\x01')
   s.write('Saving activity data...')
   time.sleep(5)
   print 'Saving activity data...'
# Record activity to database
   sql = "INSERT INTO sessionLog (sessionStartTime, sessionEndTime, type) VALUES (?,?,?)"
   cursor.execute(sql, [(start), (stopTime), (mode)]) # Need to figure out how to pull current user's ID (FK)
   db.commit()

   s.write('\xFE\x01')
   s.write('Returning to normal mode...')
   print 'Returning to normal mode...'
   normal()


# Wrong Answer **************** #
 else:
  print "*************************"	
  print 'Sorry! That is not the correct time. Try again.'
  while attempt != 5:
#   print 'Wrong answer. Try it again'
   s.write('\xFE\x01')
   s.write('Wrong answer. Try again...')
   time.sleep(1)
   
   s.write('\xFE\x01')
   s.write('Hour: Press enter when done')
   u_hr = int(raw_input("Hour: "))
   s.write('\xFE\x01')
   s.write('Minute. Press enter when done>')
   u_min = int(raw_input("Minute :"))

   time.sleep(2)
   if u_hr == h and u_min == m:
    print 'Correct! Good Job!'
    s.write('\xFE\x01')
    s.write('Correct!        Good Job!')
    correct += 1
    time.sleep(2)
    s.write('\xFE\x01')
    s.write('Try again?        1 Yes 2 No')
    
    time.sleep(1)
    control = int(raw_input('Try again? 1 Yes 2 No '))
    if control == 1:
     read()
    elif control == 2:
     stopTime = time.ctime()			# Marks end of session
 
     s.write('\xFE\x01')
     s.write('Thanks for      playing')
     time.sleep(1)

     print 'Thanks for playing.'
     time.sleep(1)
     s.write('\xFE\x01')
     s.write('Saving activity data...')
     time.sleep(5)
     print 'Saving activity data...'
# Record activity to database
     sql = "INSERT INTO sessionLog (sessionStartTime, sessionEndTime, type) VALUES (?,?,?)"
     cursor.execute(sql, [(start), (stopTime), (mode)]) # Need to figure out how to pull current user's ID (FK)
     db.commit()

     s.write('\xFE\x01')
     s.write('Returning to normal mode...')
     print 'Returning to normal mode...'
     normal()

   else:
    ++attempt
    print 'Correct answer is...'
    s.write('\xFE\x01')
    s.write('Correct answer:')
    s.write('\xFE\x90')
    s.write(hour)
    s.write('\xFE\x93')     
    s.write(min)
    time.sleep(2)
    print h, m
    print '*************************'
    read() 
# Record activity to database (show that recorded answer does not match given time)


def Set():
 global correct
 global attempt
 global sessionCount
 global sessionStart

 h = random.randrange(1,12)	
 m = random.randrange(0,59)

 print "*************************"
 s.write('\xFE\x01')
 s.write('Set Mode')
 print 'Welcome to Set Mode.'
 print "*************************"

# Time display
 #hour = "%d" % h
 #min = "%d" % m

 s.write('\xFE\x01')
 s.write('Set clock to:')
 # Play audio from voicemap
 speakTime(h,m)
 time.sleep(1)
 r_prompt = 'Set the clock to the following time:'
 
 sql = "SELECT * FROM students WHERE id=?"
 user = cursor.execute(sql, [("1")])
 start = time.ctime()				# Retrieve current time
 mode = 'Set'

 print h , m	
 print r_prompt
 s.write('\xFE\x01')
 s.write('\xFE\x80')
 s.write('Hour:             <Press Enter>')
 u_hr = int(raw_input("Hour: "))
 s.write('\xFE\x01')
 s.write('\xFE\x80')
 s.write('Minute:          <Press Enter>')
 u_min = int(raw_input("Minute :"))

 time.sleep(2)

# Student response processing
 "%02d:%02d" % (u_hr, u_min)
 res_hr = str(u_hr)
 res_min = str(u_min)
 answer = res_hr+res_min

# Correct Answer ************** #
 if u_hr == h and u_min == m:
  print 'Correct! Good Job!'
  s.write('\xFE\x01')
  s.write('Correct!        Good Job!')
  time.sleep(1)

  correct += 1
  #print correct

  sql = "INSERT INTO studentResponses (sid,studentResponse) VALUES (?,?)"
  cursor.execute(sql, [(correct), (answer)])
  db.commit()
  
  s.write('\xFE\x01')
  s.write('Try again?       (1) Yes (2) No')
  control = int(raw_input('Try again? 1 Yes 2 No '))
  if control == 1:
   Set()
  elif control == 2:
   stopTime = time.ctime()			# Marks end of session
 
   s.write('\xFE\x01')
   s.write('Thanks for      playing')
   time.sleep(1)

   print 'Thanks for playing.'
   time.sleep(1)
   s.write('\xFE\x01')
   s.write('Saving activity data...')
   time.sleep(5)
   print 'Saving activity data...'
# Record activity to database
   sql = "INSERT INTO sessionLog (sessionStartTime, sessionEndTime, type) VALUES (?,?,?)"
   cursor.execute(sql, [(start), (stopTime), (mode)]) # Need to figure out how to pull current user's ID (FK)
   db.commit()

   s.write('\xFE\x01')
   s.write('Returning to normal mode...')
   print 'Returning to normal mode...'
   normal()


# Wrong Answer **************** #
 else:
  print "*************************"	
  print 'Sorry! That is not the correct time. Try again.'
  while attempt != 5:
#   print 'Wrong answer. Try it again'
   s.write('\xFE\x01')
   s.write('Wrong answer.     Try again...')
   time.sleep(1)
   
   s.write('\xFE\x01')
   s.write('\xFE\x80')
   s.write('Hour:             <Press Enter>')
   u_hr = int(raw_input("Hour: "))
   s.write('\xFE\x01')
   s.write('\xFE\x80')
   s.write('Minute:          <Press Enter>')
   u_min = int(raw_input("Minute :"))

   time.sleep(2)
   if u_hr == h and u_min == m:
    print 'Correct! Good Job!'
    s.write('\xFE\x01')
    s.write('Correct!           Good Job!')
    correct += 1
    time.sleep(2)
    s.write('\xFE\x01')
    s.write('Try again?      (1) Yes (2) No')
    
    time.sleep(1)
    control = int(raw_input('Try again? 1 Yes 2 No '))
    if control == 1:
     read()
    elif control == 2:
     stopTime = time.ctime()			# Marks end of session
 
     s.write('\xFE\x01')
     s.write('Thanks for      playing')
     time.sleep(1)

     print 'Thanks for playing.'
     time.sleep(1)
     s.write('\xFE\x01')
     s.write('Saving activity data...')
     time.sleep(5)
     print 'Saving activity data...'
# Record activity to database
     sql = "INSERT INTO sessionLog (sessionStartTime, sessionEndTime, type) VALUES (?,?,?)"
     cursor.execute(sql, [(start), (stopTime), (mode)]) # Need to figure out how to pull current user's ID (FK)
     db.commit()

     s.write('\xFE\x01')
     s.write('Returning to normal mode...')
     print 'Returning to normal mode...'			# Return to normal mode
     normal()
 
   else:
    ++attempt
    print 'Correct answer is...'
    s.write('\xFE\x01')
    s.write('Correct answer:')
    s.write('\xFE\x90')
    s.write(hour)
    s.write('\xFE\x93')     
    s.write(min)
    time.sleep(2)
    print h, m
    print '*************************'
    Set() 

# -------------------------------------

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
  main()		# Testing whether it should go to main, or
  #modeSelect()  	# straight to quiz mode

 elif user != auth:
  print 'Invalid lunch number. Please try again....'

def userLogout():
  current = 0
# -------------------------------------

def speakTime(hour,minute):

	hour = str(hour)
	minute = str(minute)

	if minute is not "0":
		minute = re.sub("^0+","",minute)

	hour = re.sub("^0+","",hour)

	hourFile = "./VoiceMap/Hours/"+str(hour)+".wav"
	if minute is "0":
		minuteFile="./VoiceMap/Wildcard/oclock.wav"
	else:
		minuteFile="./VoiceMap/Minutes/"+str(minute)+".wav"

	playVoiceMap = "mplayer %s 1>/dev/null 2>&1 " + hourFile + " " + minuteFile
	os.system(playVoiceMap)

def main():
 normal()
# modeSelect()

main()
