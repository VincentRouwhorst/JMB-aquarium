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
from datetime import datetime
import json
import chardet
import RPi.GPIO as GPIO

#DOMOTICZ_IP = 'http://127.0.0.1:8080'
DOMOTICZ_IP = 'http://192.168.5.2:8080'

# GPIO Setup Raspberry Pi PWM pins
GPIO.setmode(GPIO.BOARD)

def StartPWM():
   global pwm12
   # Setup GPIO Pins
   GPIO.setup(12, GPIO.OUT)
   #GPIO.setup(32, GPIO.OUT)
   #GPIO.setup(33, GPIO.OUT)
   #GPIO.setup(35, GPIO.OUT)

   # Set PWM instance and their frequency
   pwm12 = GPIO.PWM(12, 200)
   #pwm32 = GPIO.PWM(32, 400)
   #pwm33 = GPIO.PWM(33, 400)
   #pwm35 = GPIO.PWM(35, 400)

   # Start PWM with 0% Duty Cycle, OFF state
   pwm12.start(0)
   #pwm32.start(0)
   #pwm33.start(0)
   #pwm35.start(0)

def StopPWM():
   global pwm12
   pwm12.stop(0)
   #pwm32.stop(0)
   #pwm33.stop(0)
   #pwm35.stop(0)
   # Cleans the GPIO
   GPIO.cleanup()

def getSetting(id):
   global id_name
   try:
       #print(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(id_name[id]["idx"]))
       r = requests.get(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(id_name[id]["idx"]))
       siteresponse = r.json()
       if (r.ok): # response check is ok
          DeviceLevel = int(siteresponse['result'][0]['Level'])
          #print(DeviceLevel)
          DeviceState = siteresponse['result'][0]['Data']
          #print(DeviceState)
          DeviceLastUpdate = siteresponse['result'][0]['LastUpdate'].replace('-', '/')
          DeviceLastUpdate = datetime.strptime(DeviceLastUpdate, "%Y/%m/%d %H:%M:%S")
          DeltaDate = id_name[id]["lastupdate"] - DeviceLastUpdate
          #print("mem " + str(id_name[id]["lastupdate"]) + " -  read " + str(DeviceLastUpdate) + " = " + str(DeltaDate))
          if DeltaDate.total_seconds() == 0 :
            id_name[id]["changed"] = 0
          else:
            id_name[id]["changed"] = 1
            print("Updated : " + str(id_name[id]["lastupdate"]))
            id_name[id]["lastupdate"] = DeviceLastUpdate
          #print(id_name[id]["changed"])
          #
          if DeviceState == "Off":
            return 0
            id_name[id]["lastlevel"] = 0
          elif DeviceState == "On":
            return 100
          elif DeviceLevel >= 0 and DeviceLevel <= 100: # Extra safety levels must be between 0 and 100
            return DeviceLevel
            id_name[id]["lastlevel"] = Devicelevel
          else:
            return 0
            id_name[id]["lastlevel"] = 0
       else: # response check failed
          return 0
          id_name[id]["lastlevel"] = 0
   except Exception as e:
       print("Oeps an Error")
       print(f"NOT OK: {str(e)}")
       return 0
       id_name[id]["lastlevel"] = 0

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
  id_name = {"JMB-C1":      {"idx" : 7297, "lastupdate" : '', "lastlevel" : '', "changed" : 1}, 
             "JMB-C2":      {"idx" : 7298, "lastupdate" : '', "lastlevel" : '', "changed" : 1}, 
             "JMB-C3":      {"idx" : 7299, "lastupdate" : '', "lastlevel" : '', "changed" : 1}, 
             "JMB-C4":      {"idx" : 7300, "lastupdate" : '', "lastlevel" : '', "changed" : 1}, 
             "JMB-C5":      {"idx" : 7301, "lastupdate" : '', "lastlevel" : '', "changed" : 1}, 
             "JMB-SunUp":   {"idx" : 7304, "lastupdate" : '', "lastlevel" : '', "changed" : 1}, 
             "JMB-SunDown": {"idx" : 7305, "lastupdate" : '', "lastlevel" : '', "changed" : 1}}
  for key in sorted(id_name):
     id_name[key]["lastupdate"] = datetime.now()
  
  StartPWM()
  try:
     while True:
        for key in sorted(id_name):
           getSetting(key)
           #   print("key = " + key)
           #   print(getSetting(key))
           #PushSetting("JMB-C1", 100)
           if id_name[key]["changed"] == 1:
             print("UPDATE PWM SETTINGS : " + key)
             pwm12.ChangeDutyCycle(getSetting(key))
             #pwm32.ChangeDutyCycle(getSetting(id_name["JMB-C2"]["idx"]))
             #pwm33.ChangeDutyCycle(getSetting(id_name["JMB-C3"]["idx"]))
             #pwm35.ChangeDutyCycle(getSetting(id_name["JMB-C4"]["idx"]))
        #time.sleep(2)
  except KeyboardInterrupt:
     StopPWM()
     #pwm12.stop()
     # Cleans the GPIO
     #GPIO.cleanup()
########### Work in progress ############
