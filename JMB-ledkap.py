#!/usr/bin/python --------------------------------------
#
#              JMB-ledkap.py
#
# JMB Seawater Raspberry PI ledcontroller
# With Domoticz integration
#
# Author : Vincent Rouwhorst
# Date   : 31/12/2021
#
# Domoticz Json documentation
# https://www.domoticz.com/wiki/Domoticz_API/JSON_URL's#Custom_Sensor
#--------------------------------------

import requests
import time
#import datetime
import json
import chardet
import RPi.GPIO as GPIO

DOMOTICZ_IP = 'http://127.0.0.1:8080'

# GPIO Setup Raspberry Pi PWM pins
#GPIO.setmode(GPIO.BOARD)

# Setup GPIO Pins
#GPIO.setup(12, GPIO.OUT)
#GPIO.setup(32, GPIO.OUT)
#GPIO.setup(33, GPIO.OUT)
#GPIO.setup(35, GPIO.OUT)

# Set PWM instance and their frequency
#pwm12 = GPIO.PWM(12, 400)
#pwm32 = GPIO.PWM(32, 400)
#pwm33 = GPIO.PWM(33, 400)
#pwm35 = GPIO.PWM(35, 400)

# Start PWM with 0% Duty Cycle, OFF state
#pwm12.start(0)
#pwm32.start(0)
#pwm33.start(0)
#pwm35.start(0)


def getSetting(id):
   #global id_name
   #id_name[id]
   try:
       #print(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(id))
       r = requests.get(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(id))
       siteresponse = r.json()
       if (r.ok): # response check is ok
          DeviceLevel = int(siteresponse['result'][0]['Level'])
          #print(DeviceLevel)
          DeviceState = siteresponse['result'][0]['Data']
          #print(DeviceState)
          DeviceLastUpdate = siteresponse['result'][0]['LastUpdate']
          print(DeviceLastUpdate)
          print(type(DeviceLastUpdate))
          if DeviceState == "Off":
            return 0
          elif DeviceState == "On":
            return 100
          elif DeviceLevel >= 0 and DeviceLevel <= 100: # Extra safety levels must be between 0 and 100
            return DeviceLevel
          else:
            return 0
       else: # response check failed
          return 0
   except Exception as e:
       print("Oeps an Error")
       print(f"NOT OK: {str(e)}")
       return 0

def PushSetting(id, leveltoset):
   # Push settings to Domoticz
   # Set a dimmable light to a certain level
   # /json.htm?type=command&param=switchlight&idx=99&switchcmd=Set%20Level&level=6
   #
   try:
       print(DOMOTICZ_IP + "/json.htm?type=command&param=switchlight&idx=" + str(id) + "&switchcmd=Set%20Level&level=" + str(leveltoset))
       r = requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=switchlight&idx=" + str(id) + "&switchcmd=Set%20Level&level=" + str(leveltoset))
       siteresponse = r.json()
       if (r.ok): # response check is ok
          print("OK")
   except Exception as e:
       print("Oeps an Error")
       print(f"NOT OK: {str(e)}")
       return 0



if __name__ == '__main__':
  # Script has been called directly

  # Dictionary of switches to process, the key is for debuging
  id_name = {"JMB-C1":      {"idx" : 7297, "lastupdate" : '', "lastlevel" : ''}, 
             "JMB-C2":      {"idx" : 7298, "lastupdate" : '', "lastlevel" : ''}, 
             "JMB-C3":      {"idx" : 7299, "lastupdate" : '', "lastlevel" : ''}, 
             "JMB-C4":      {"idx" : 7300, "lastupdate" : '', "lastlevel" : ''}, 
             "JMB-C5":      {"idx" : 7301, "lastupdate" : '', "lastlevel" : ''}, 
             "JMB-SunUp":   {"idx" : 7304, "lastupdate" : '', "lastlevel" : ''}, 
             "JMB-SunDown": {"idx" : 7305, "lastupdate" : '', "lastlevel" : ''}}
  
  for key in sorted(id_name):
     print(key)
     print(getSetting(id_name[key]["idx"]))
  PushSetting(id_name["JMB-C1"]["idx"], 100)
  #pwm12.ChangeDutyCycle(getSetting(id_name["JMB-C1"]["idx"]))
  #pwm32.ChangeDutyCycle(getSetting(id_name["JMB-C2"]["idx"]))
  #pwm33.ChangeDutyCycle(getSetting(id_name["JMB-C3"]["idx"]))
  #pwm35.ChangeDutyCycle(getSetting(id_name["JMB-C4"]["idx"]))
  #time.sleep(10)
  #pwm35.stop()
  # Cleans the GPIO
  #GPIO.cleanup()
########### Work in progress ############
  #while True:
