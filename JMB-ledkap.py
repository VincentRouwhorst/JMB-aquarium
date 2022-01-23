#! /usr/bin/env python3
#--------------------------------------
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
#Must start "sudo systemctl start pigpiod"

import requests, time, json, chardet, pigpio
from datetime import datetime

#DOMOTICZ_IP = 'http://127.0.0.1:8080'
DOMOTICZ_IP = 'http://192.168.5.2:8080'

# GPIO Setup Raspberry Pi PWM pins
#GPIO.setmode(GPIO.BOARD)
pi = pigpio.pi()


def UpdatePWM(id, dc):
   #HardwarePWM = [12, 13, 18, 19]   # 12/13/18/19 Raspberry PI 2 hardware PWM pins
   #print("UpdatePWM : " + str(id) + " : " + str(dc) + " pin = " + str(id_name[id]["pin"]) + " changed = " + str(id_name[id]["changed"]) + "  lastlevel = " + str(id_name[id]["lastlevel"]))
   #if id_name[id]["pin"] in HardwarePWM:
   #   dc= dc * 10000  # duty cycle is 10 % * 10000
   #   pi.hardware_PWM(id_name[id]["pin"], 200, dc) # gpio pin, freq, duty cycle
   #else:
      #software PWM user_gpio:= 0-31
      #dutycycle:= 0-range (range defaults to 255).
   if id_name[id]["changed"] == 1 :
      dc = (255/100) * dc
      pi.set_PWM_frequency(id_name[id]["pin"], 200)  # set freq
      pi.set_PWM_dutycycle(id_name[id]["pin"], dc)   # set duty cycle


#def StopPWM():
   # Cleans the GPIO
   #pi.stop()

def getSetting(id):
   global id_name
   try:
       #print(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(id_name[id]["idx"]))
       r = requests.get(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(id_name[id]["idx"]))
       siteresponse = r.json()
       if (r.ok): # response check is ok
          DeviceLevel = int(siteresponse['result'][0]['Level'])
          #print("Level" + str(DeviceLevel))
          DeviceState = siteresponse['result'][0]['Data']
          #print("State" + str(DeviceState))
          DeviceLastUpdate = siteresponse['result'][0]['LastUpdate'].replace('-', '/')
          DeviceLastUpdate = datetime.strptime(DeviceLastUpdate, "%Y/%m/%d %H:%M:%S")
          DeltaDate = id_name[id]["lastupdate"] - DeviceLastUpdate
          #print("mem " + str(id_name[id]["lastupdate"]) + " -  read " + str(DeviceLastUpdate) + " = " + str(DeltaDate))
          if DeltaDate.total_seconds() == 0 :
            id_name[id]["changed"] = 0
          else:
            id_name[id]["changed"] = 1
            print("Updated : " + str(id) + "  Level = " + str(DeviceLevel) + "  Time = " + str(id_name[id]["lastupdate"]))
            id_name[id]["lastupdate"] = DeviceLastUpdate
          #print(id_name[id]["changed"])
          #
          if DeviceState == "Off":
            return 0
            id_name[id]["lastlevel"] = 0
          elif DeviceState == "On":   # DeviceLevel eg "On" and "Level" : 48
            return DeviceLevel
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

def SunUP(id):
   if id == 100:
      global id_name
      countdowntimer = 15 * 60 # 15 min * 60 sec = 900 sec
      lamplevel = 100 # 0-100
      for x in range(lamplevel):
         print("SunUP")
         time.sleep(countdowntimer/lamplevel)
         return 1, x
      return 0, 100


if __name__ == '__main__':
  # Script has been called directly

  # Dictionary of switches to process, the key is for debuging
  # for reference see cli pinout command
  id_name = {"JMB-C1":      {"idx" : 7297, "lastupdate" : '', "lastlevel" : '', "changed" : 1, "pin" : 12 },
             "JMB-C2":      {"idx" : 7298, "lastupdate" : '', "lastlevel" : '', "changed" : 1, "pin" : 13 },
             "JMB-C3":      {"idx" : 7299, "lastupdate" : '', "lastlevel" : '', "changed" : 1, "pin" : 18 },
             "JMB-C4":      {"idx" : 7300, "lastupdate" : '', "lastlevel" : '', "changed" : 1, "pin" : 19 },
             "JMB-C5":      {"idx" : 7301, "lastupdate" : '', "lastlevel" : '', "changed" : 1, "pin" : 4 },
             "JMB-SunUp":   {"idx" : 7304, "lastupdate" : '', "lastlevel" : '', "changed" : 1, },
             "JMB-SunDown": {"idx" : 7305, "lastupdate" : '', "lastlevel" : '', "changed" : 1, }}
  # fill Dict with datetime and startup
  for key in sorted(id_name):
     id_name[key]["lastupdate"] = datetime.now()
  # end fill Dict

  UpdatePWM("JMB-C1", 0) # start at level 0%
  try:
     while True:
        for key in sorted(id_name):
           if key.startswith("JMB-C"):
              #getSetting(key)
              UpdatePWM(key, getSetting(key))
           elif key.startswith("JMB-SunU"):
              getSetting(key)
              #print(key + " - " + str(getSetting(key)))
              #print(str(datetime.now() - id_name[key]["lastupdate"]))
              #if id_name[key]["changed"] == 1:
              #   print(key + " Delay proces ")
              #   print(str(id_name[key]["changed"]))
              #   print(str(id_name[key]["lastlevel"]))
           #   print("key = " + key)
           #   print(getSetting(key))
           #PushSetting("JMB-C1", 100)
           #if id_name[key]["changed"] == 1:
             #print("UPDATE PWM SETTINGS : " + key)
             #pwm12.ChangeDutyCycle(getSetting(key))
             #pwm32.ChangeDutyCycle(getSetting(id_name["JMB-C2"]["idx"]))
             #pwm33.ChangeDutyCycle(getSetting(id_name["JMB-C3"]["idx"]))
             #pwm35.ChangeDutyCycle(getSetting(id_name["JMB-C4"]["idx"]))
           time.sleep(0.1)
  except KeyboardInterrupt:
     pi.stop() # Cleans the GPIO and Disconnect from local Pi
     print(" --== ByeBye ==-- ")
########### Work in progress ############
