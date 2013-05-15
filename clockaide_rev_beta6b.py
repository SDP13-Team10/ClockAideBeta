#!/usr/bin/python

# ClockAide System
# User Login, LCD display
# 4/6/13 Voice map, set mode, fixed time display
# 4/7/13 Fixed voice prompt in Set mode, Adjusted displays for both read and set
#	 User login system functional
# 4/8/13 User login goes to normal mode, based on feedback from demo to professor
# 4/10/13 Added score for each session. Currently shows zero (may need floating point support)
# 4/22/13 Added changes to time display and wrong answer display from rev. 5b
# 4/22/13 Extracted from rev 5c
# 5/2/13  Moved database updates from revision 5c

import time, datetime, sys, random, sqlite3, string, usb, serial, os, datetime, re, shutil, errno

#---------------------------------
# Tracking system
id = 0
correct = 0
incorrect = 0
questions = 0
attempt = 0
sessionCount = 0
sessionStart = 0
lockout = 0		# Login attempts

#----------------------------------
# Database initialization
db = sqlite3.connect("./Database/ClockAideDB")
cursor = db.cursor()


#----------------------------------
# LCD Display
s = serial.Serial(port = '/dev/ttyAMA0', baudrate = 9600)
# x80 is the first spot on line 1
# x90 is the first spot on line 2

#---------------------------------- Turned off in this revision. Used in Revision 6
# Motor Initialization
motor = serial.Serial(port = '/dev/ttyACM0', baudrate = 9600) 	# Alternate location /dev/ttyUSB0 or /dev/ttyACM0


#----------------------------------
# Keypad detection (DEPRECATED 4/3/13)
keypad = serial.Serial()

#---------------------------------
#Normal Mode
greeting = "Welcome to ClockAide!"
mode = "Normal Mode"

def normal():
 global sessionCount
 global id

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
 motor.write(getDateTimeString())
 time.sleep(5)		# Sends signal to motor circuit to wake up
 print getDateTimeString()
# print clock

 print hourNow, minuteNow, modulation		# Send time to stepper motors
 #motor.write(getDateTimeString())    # Original line, repeated. Testing to see if 2nd call wakes up motors
 
 speakTime(hourNow,minuteNow) 
 
 time.sleep(2)
 s.write('\xFE\x01')
 s.write(clock)

 time.sleep(5)
 s.write('\xFE\x01')
 s.write('\xFE\x0D')				# Turns on blinking cursor
 s.write('Quiz Mode?      (1) Yes (2) No')
 control = int(raw_input("Key pressed: "))
 if control == 1:
  s.write('\xFE\x0C')
  userLogin()				
  #modeSelect()
 elif control == 2:
  quit()

 elif control == 8:					# User prompt to speak current time
  normal()

 elif control == 0:
  #print 'Programming Mode'
  #adminLogin()
  s.write('\xFE\x01')
  s.write('ID Programming Mode')
  prog()

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
 s.write('\xFE\x0D')
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

 global questions
 global correct		# In python, this is required to tell the interpreter
 global incorrect	# to use the definition at the top of the program
 global attempt		
 global sessionCount
 global sessionStart
 global id

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

 questions += 1
 print questions
 s.write('\xFE\x01')
 s.write('What time is it?')
 time.sleep(1)
 r_prompt = 'What time is it?'

 sql = "SELECT * FROM students WHERE id=?"
 user = cursor.execute(sql, [("1")])
 start = time.ctime()				# Retrieve current time
 mode = 'Read'

# Move stepper motors here
 command = str(2)
 motor.write(command)	# Signals motor circuit to receive hour and minute from Pi
 hourCh = chr(h)
 minCh = chr(m)
 motor.write(hourCh)
 motor.write(minCh)

 print r_prompt

 s.write('\xFE\x01')
 print h, m	# For debugging purposes only
 s.write('\xFE\x80')
 s.write(hour)
 s.write('\xFE\x82')
 s.write(':')
 s.write('\xFE\x83')
 s.write(min)
 time.sleep (2)

 s.write('\xFE\x01')
 s.write('\xFE\x80')
 s.write('Hour:')
 u_hr = int(raw_input("Hour: "))
 s.write('\xFE\x01')
 s.write('\xFE\x80')
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
  s.write('\xFE\x0C')
  s.write('Correct!        Good Job!')
  time.sleep(1)

  correct += 1
  print correct

  sql = "INSERT INTO studentResponses (sid,studentResponse) VALUES (?,?)"
  cursor.execute(sql, [(correct), (answer)])
  db.commit()
  
  s.write('\xFE\x01')
  s.write('\xFE\x0D')
  s.write('Try again?       (1) Yes (2) No')
  control = int(raw_input('Try again? 1 Yes 2 No '))
  if control == 1:
   read()
  elif control == 2:
   stopTime = time.ctime()			# Marks end of session
 
   s.write('\xFE\x01')
   s.write('Thanks for      playing')
   time.sleep(1)

   print 'Thanks for playing.'
   score = (correct/questions)
   time.sleep(1)
   s.write('\xFE\x01')
   s.write('Saving activity data...')
   time.sleep(5)
   print 'Saving activity data...'
# Record activity to database
   sql = "INSERT INTO sessionLog (id, sessionStartTime, sessionEndTime, type, score) VALUES (?,?,?,?,?)"
   cursor.execute(sql, [(id), (start), (stopTime), (mode), (score)]) # Need to figure out how to pull current user's ID (FK)
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
   s.write('Wrong answer...    Try again')
   time.sleep(1)
   
   s.write('\xFE\x01')
   s.write('\xFE\x0D')
   s.write('Hour: Press      enter when done')
   u_hr = int(raw_input("Hour: "))
   s.write('\xFE\x01')
   s.write('Minute: Press   enter when done')
   u_min = int(raw_input("Minute :"))

   time.sleep(2)
   if u_hr == h and u_min == m:
    print 'Correct! Good Job!'
    s.write('\xFE\x01')
    s.write('\xFE\x0C')
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
     score = (correct/questions)
     time.sleep(1)
     s.write('\xFE\x01')
     s.write('Saving activity data...')
     time.sleep(5)
     print 'Saving activity data...'
# Record activity to database
     sql = "INSERT INTO sessionLog (id, sessionStartTime, sessionEndTime, type, score) VALUES (?,?,?,?,?)"
     cursor.execute(sql, [(id), (start), (stopTime), (mode), (score)]) # Need to figure out how to pull current user's ID (FK)
     db.commit()

     s.write('\xFE\x01')
     s.write('Returning to normal mode...')
     print 'Returning to normal mode...'
     normal()

   else:
    ++attempt
    incorrect += 1
    print incorrect
    print 'Correct answer is...'
    s.write('\xFE\x01')
    s.write('Correct answer:')
    time.sleep(1)
    s.write('\xFE\x01')
    s.write('\xFE\x84')
    s.write(hour)
    s.write('\xFE\x85')
    s.write(':')
    s.write('\xFE\x86')   
    s.write(min)
    time.sleep(2)
    print h, m
    print '*************************'
    read() 
# Record activity to database (show that recorded answer does not match given time)


def Set():

 global questions
 global correct
 global incorrect
 global attempt
 global sessionCount
 global sessionStart
 global id

 h = random.randrange(1,12)	
 m = random.randrange(0,59)

 print "*************************"
 s.write('\xFE\x01')
 s.write('Set Mode')
 print 'Welcome to Set Mode.'
 print "*************************"

# Time display
 hour = "%d" % h
 min = "%d" % m

 questions += 1
 s.write('\xFE\x01')
 s.write('Set clock to:')
 s.write('\xFE\x0D')
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
 s.write('\xFE\x0D')
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
  s.write('\xFE\x0C')
  s.write('Correct!        Good Job!')
  time.sleep(1)

  correct += 1
  #print correct

  sql = "INSERT INTO studentResponses (sid,studentResponse) VALUES (?,?)"
  cursor.execute(sql, [(correct), (answer)])
  db.commit()
  
  s.write('\xFE\x01')
  s.write('\xFE\x0D')
  s.write('Try again?       (1) Yes (2) No')
  control = int(raw_input('Try again? 1 Yes 2 No '))
  if control == 1:
   Set()
  elif control == 2:
   stopTime = time.ctime()			# Marks end of session
 
   s.write('\xFE\x01')
   s.write('\xFE\x0C')
   s.write('Thanks for      playing')
   time.sleep(1)

   print 'Thanks for playing.'
   score = (correct/questions)
   time.sleep(1)
   s.write('\xFE\x01')
   s.write('Saving activity data...')
   time.sleep(5)
   print 'Saving activity data...'
# Record activity to database
   sql = "INSERT INTO sessionLog (id, sessionStartTime, sessionEndTime, type, score) VALUES (?,?,?,?,?)"
   cursor.execute(sql, [(id), (start), (stopTime), (mode), (score)]) # Need to figure out how to pull current user's ID (FK)
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
    s.write('\xFE\x0C')
    s.write('Correct!           Good Job!')
    correct += 1
    time.sleep(2)
    s.write('\xFE\x01')
    s.write('\xFE\x0D')
    s.write('Try again?      (1) Yes (2) No')
    
    time.sleep(1)
    control = int(raw_input('Try again? 1 Yes 2 No '))
    if control == 1:
     read()
    elif control == 2:
     stopTime = time.ctime()			# Marks end of session
 
     s.write('\xFE\x01')
     s.write('\xFE\x0C')
     s.write('Thanks for      playing')
     time.sleep(1)

     print 'Thanks for playing.'
     score = (correct/questions)
     time.sleep(1)
     s.write('\xFE\x01')
     s.write('Saving activity data...')
     time.sleep(5)
     print 'Saving activity data...'
# Record activity to database
     sql = "INSERT INTO sessionLog (id, sessionStartTime, sessionEndTime, type, score) VALUES (?,?,?,?,?)"
     cursor.execute(sql, [(id), (start), (stopTime), (mode), (score)]) # Need to figure out how to pull current user's ID (FK)
     db.commit()

     s.write('\xFE\x01')
     s.write('Returning to normal mode...')
     print 'Returning to normal mode...'			# Return to normal mode
     normal()
 
   else:
    ++attempt
    incorrect += 1
    print 'Correct answer is...'
    s.write('\xFE\x01')
    s.write('Correct answer:')
    time.sleep(1)
    s.write('\xFE\x01')
    s.write('\xFE\x84')
    s.write(hour)
    s.write('\xFE\x85')
    s.write(':')
    s.write('\xFE\x86')     
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

 s.write('\xFE\x0C')
 print 'What would you like to do?'
 s.write('\xFE\x01')
 s.write('Programming Mode')
 time.sleep(2)

 print '1: Add user 2: Delete User 3: Export users 4: Export Session Log 5: Export Activity data 6: Backup Database'
 
 s.write('\xFE\x01')
 s.write('1: Add user     2: Delete user  ')
 time.sleep(2)
 s.write('\xFE\x01')
 s.write('3: Export users 4: Export Logs') 
 time.sleep(2)
 s.write('\xFE\x01')
 s.write('5: Export usage 6: Backup dB') 
 time.sleep(2)
 s.write('\xFE\x01')
 s.write('7: Save database') 
 time.sleep(1)

 s.write('\xFE\x01')
 s.write('\xFE\x0D')
 s.write('Choose an option')


 option = int(raw_input("Option: ")) #Cast required 

 if option == 0:
  prog()

 elif option == 1:
  print 'Enter lunch number'
  s.write('\xFE\x01')
  s.write('\xFE\x0D')
  s.write('New lunch number <Press Enter>')
  ID_input = int(raw_input("Lunch Number: ")) #Cast required
  s.write('\xFE\x01')
  s.write('\xFE\x0D')
  s.write('Enter student   name:')
  name = raw_input("Name: ")
  
  s.write('\xFE\x01')
  s.write('New User        ' + name)
  time.sleep(2)
  sql = "INSERT INTO students (id, Name) VALUES (?,?)"
  cursor.execute(sql, [(ID_input), (name)])
  db.commit()
  
  prog()
  
 elif option == 2:					# Delete user: not working - check syntax
  print 'Enter lunch number'
  s.write('\xFE\x01')
  s.write('\xFE\x0D')
  s.write('ID to remove     <Press Enter>')
  ID_input = int(raw_input("Lunch Number: ")) #Cast required
  
  s.write('\xFE\x01')
  s.write('\xFE\x0D')
 
  s.write('\xFE\x01')
  s.write(' Removed user ')
  time.sleep(2)
#  cursor.execute(DELETE * FROM students WHERE id=+ID_input)
#  sql = "DELETE FROM students (id, Name) VALUES (?,?)"
 # cursor.execute(sql, [(ID_input), (name)])
  db.commit()
  
  prog()

 elif option == 3:
  s.write('\xFE\x01')
  s.write('Saving lunch    numbers to Flash')		# User List Export
  time.sleep(2)
  dbUsers()
  time.sleep(1)
  normal()

 elif option == 4:
  s.write('\xFE\x01')
  s.write('Saving session  log to Flash...')		# Session Log Export	
  time.sleep(2)
  dbSessionLog()
  time.sleep(1)
  normal()

 elif option == 5:
  s.write('\xFE\x01')
  s.write('Saving quiz usage to Flash...')		# Activity Data Export	
  time.sleep(2)
  dbActivity()
  time.sleep(1)
  normal()

 elif option == 6:
  s.write('\xFE\x01')
  s.write('Initializing Database Backup...')		# Database backup	
  time.sleep(2)
  dbBackup()
  time.sleep(1)
  normal()

 elif option == 7:					# Database export
  s.write('\xFE\x0C')
  s.write('\xFE\x01')
  s.write('Saving database')
  #subprocess.Popen(["/usr/bin/bash", "dbsave_test", "var = 11; ignore all", .])
  subprocess.Popen(['./Database/dbsave_test "var = 11; ignore all", /home/pi/Software/Database'], shell = True)

  time.sleep(1)
  normal() 

 elif option == 8:
  s.write('\xFE\x0C')
  s.write('\xFE\x01')
  s.write('Returning to    normal mode ...')
  time.sleep(1)
  normal()
# -------------------------------------
# Is not used at all in the program
def insertSessionData(start, user, sessionEnd):
 sessionStart = time.ctime()
 user = cursor.execute("SELECT * FROM students WHERE ID = 1234")
 sessionEnd = 0
 mode = "Read"

# -------------------------------------
def userLogin():
 global lockout
 global id

 s.write('\xFE\x01')
 s.write('\xFE\x0D')
# s.write('User Login      Enter Lunch #:')
 s.write('Enter Lunch #:')
 user = int(raw_input("Enter your lunch number: "))

 
 sql = "SELECT id FROM students WHERE id=?"
 auth = cursor.execute(sql, [(user)])
 userInput = str(user)
 cursor.execute('''SELECT * FROM students WHERE id='''+userInput)
 queryResult = cursor.fetchone()

 if queryResult is None:
 	queryResult = [-1,"-1"]

 if queryResult[0] == user:
   print "Welcome " + queryResult[1]
   print 'User authenticated. Starting ClockAide....'
   s.write('\xFE\x01')
   s.write('\xFE\x0C')
   s.write('     User         Authenticated')
   time.sleep(2)
   id = user
   #normal()
   modeSelect()		# Was switched back so that different users can log in
			# Placed a call for this in Normal mode

 elif lockout != 3:
    lockout += 1
    print 'Invalid lunch number. Please try again....'
    s.write('\xFE\x01')
    s.write('Login Failed.   Try again...')
    time.sleep(1)
    userLogin()

 else:
   print 'Maximum attempts reached. Returning to normal mode...'
   s.write('\xFE\x01')
   s.write('Maximum attempts reached....')
   time.sleep(3)
   s.write('\xFE\x01')
   s.write('Returning to Normal Mode...')
   time.sleep(1)
   normal()
# -------------------------------------

# -------------------------------------
# Protects the software from blank and inappropriate inputs from the user

#def keyFilter(input)

# if input == None:
  
# -------------------------------------
# Might not be used
def userLogout():
  current = 0
# -------------------------------------

def getDateTimeString():
        currentTime = datetime.datetime.now()
        #print(currentTime.strftime("%I%M"))
        return currentTime.strftime("%H, %M, %S, %d, %m, %Y")

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

# -------------------------------------
# Perform periodic backups of database for easy recovery

def dbBackup():
 src = "./Database/ClockAideDB"
 dst = "../../../../media/PENDRIVE_" 	# Will have to use a USB drive with the clockaide volume label

 fileCopy(src, dst)
 print "Database Backup Successful"
 s.write('\xFE\x01')
 s.write('Database Backup Successful')


def fileCopy(src, dst):
 if dst != None:
  shutil.copy(src, dst)			# This will overwrite the file if it exists
  print "Copy Successful"
  s.write('\xFE\x01')
  s.write('Copy Successful')
  time.sleep(1)

 else:
  print "Copy unsuccessful. Please try again."
  s.write('\xFE\x01')
  s.write('Copy unsuccessful. Please try again')
  time.sleep(1)

# Activity data (Student Responses) -------------------
def dbActivity():
 src = "./Database/Activity.csv"
 dst = "../../../../media/PENDRIVE" 

 fileCopy(src, dst)
 print "Activity data Export Successful"
 s.write('\xFE\x01')
 s.write('Activity data export Successful')

# Class List ----------------------
def dbUsers():
 src = "./Database/users.csv"
 dst = "../../../../media/PENDRIVE" 

 fileCopy(src, dst)
 print "User List Exported"
 s.write('\xFE\x01')
 s.write('User list         exported')

# Session Log ----------------
def dbSessionLog():
 src = "./Database/sessionLog.csv"
 dst = "../../../../media/PENDRIVE" 

 fileCopy(src, dst)
 print "Session Log Exported"
 s.write('\xFE\x01')
 s.write('Session Log exported')



def main():
 #userLogin()
 normal()
# modeSelect()

main()
