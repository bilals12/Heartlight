import os
import RPi.GPIO as GPIO
from sys import exit
import time
from time import strftime
from datetime import datetime
import subprocess
from subprocess import Popen
# set GPIO mode to BCM
# taking GPIO number instead of pin number
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # removes warnings

GPIO.setup(23, GPIO.IN) #initialize receiver GPIO to take input
GPIO.setup(24, GPIO.OUT) # initialize LED GPIO to give output

GPIO.output(24, 0) # start with LED on

GPIO.add_event_detect(23, GPIO.RISING) # initializing our "Rising Edge" function for GPIO 23
try:
	firstBeatTime = time.time() # initializing to internal clock
	sampleCounter = 0
	bpm = 0
	alarm_HH = input("Enter the hour you wanna wake up at: ")
        alarm_MM = input ("Enter the minute: ")
        print("Alarm set at: {0:02}:{1:02}").format(alarm_HH, alarm_MM)
	hours = int(alarm_HH)
	minutes = int(alarm_MM)
	song_path = '/home/pi/goodmorning.mp3'
	while True:
		now = time.localtime()
		if (now.tm_hour == hours and now.tm_min == minutes):
			print("Wakey wakey, eggs 'n bakey!")
			subprocess.Popen(['mplayer',song_path],stdin=subprocess.PIPE,shell=True)	
		if time.time() < firstBeatTime + 60:	# performing this loop in the interval of 1 min (60 seconds) after the first beat is detected
			if GPIO.event_detected(23): # if rising edge is detected at GPIO 23
				GPIO.output(24,0)	# LED ON
				sampleCounter = sampleCounter + 1 # increment sample counter every time a signal is received in that minute. after 1 min, it should be the BPM
				time.sleep(0.01) # delay
		 
				
		else:
			bpm = sampleCounter # after 1 min, BPM is now the same as the sampleCounter value
 			firstBeatTime = time.time() # reset firstBeatTime to internal clock
			sampleCounter = 0 # reset sample counter so that it may start fresh
			print ("BPM: %s") %(bpm) # print the heartrate
			if bpm < 50: # if heartrate is less than 50 BPM
				GPIO.output(24, 1) # light goes off
			else:
				GPIO.output(24, 0) # otherwise light stays on

# end script with ctrl+c
except KeyboardInterrupt:
	quit("Done!")
