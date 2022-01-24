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
##Must start "sudo systemctl start pigpiod"
# enable at boot "sudo systemctl enable pigpiod"

import requests, time, json, chardet, pigpio
from datetime import datetime, timedelta

#DOMOTICZ_IP = 'http://127.0.0.1:8080'
DOMOTICZ_IP = 'http://192.168.5.2:8080'

# GPIO Setup Raspberry Pi PWM pins
#GPIO.setmode(GPIO.BOARD)
pi = pigpio.pi()


def UpdatePWM(id, dc):
   #HardwarePWM = [12, 13, 18, 19]   # 12/13/18/19 Raspberry PI 2 hardware PWM pins
   #print("UpdatePWM : " + str(id) + " : " + str(dc) + " pin = " + str(id_name[id]["pin"]) + " changed = " + str(id_name[id]["changed"]) + "  lastlevel = " + str(id_name[id]["lastlevel"]))
   if id_name[id]["changed"] == 1 :
      dc = (255/100) * dc   #100% dutycycle:= 0-range (range defaults to 255).
      pi.set_PWM_frequency(id_name[id]["pin"], 200)  # set freq
      pi.set_PWM_dutycycle(id_name[id]["pin"], dc)   # set duty cycle


def getSetting(id):
   #global firststart
   try:
       #print(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(id_name[id]["idx"]))
       r = requests.get(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(id_name[id]["idx"]))
       siteresponse = r.json()
       if (r.ok): # response check is ok
          DeviceLevel = int(siteresponse['result'][0]['Level'])
          #print("Level" + str(DeviceLevel))
          DeviceState = siteresponse['result'][0]['Data']
          id_name[id]["DeviceState"] = DeviceState
          #print("State" + str(DeviceState))
          DeviceLastUpdate = siteresponse['result'][0]['LastUpdate'].replace('-', '/')
          DeviceLastUpdate = datetime.strptime(DeviceLastUpdate, "%Y/%m/%d %H:%M:%S")
          DeltaDate = id_name[id]["lastupdate"] - DeviceLastUpdate
          #DeltaFirststart = datetime.now() - firststart
          #print(str(DeltaFirststart.total_seconds()))
          #print("mem " + str(id_name[id]["lastupdate"]) + " -  read " + str(DeviceLastUpdate) + " = " + str(DeltaDate))
          if DeltaDate.total_seconds() == 0 :
            id_name[id]["changed"] = 0
          #elif DeltaFirststart.total_seconds() <= 5 and id == "JMB-SunUp":   # for first run do not start SunControl
          #  id_name[id]["changed"] = 0
          else:   # regular change
            id_name[id]["changed"] = 1
            print("Updated : " + str(id) + "  Level = " + str(DeviceLevel) + "  Time = " + str(id_name[id]["lastupdate"]))
            id_name[id]["lastupdate"] = DeviceLastUpdate
            id_name[id]["LastupdateLocal"] = datetime.now()
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
       #print(DOMOTICZ_IP + "/json.htm?type=command&param=switchlight&idx=" + str(id) + "&switchcmd=Set%20Level&level=" + str(leveltoset))
       r = requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=switchlight&idx=" + str(id) + "&switchcmd=Set%20Level&level=" + str(leveltoset))
       siteresponse = r.json()
       #if (r.ok): # response check is ok
       #   print("OK")
   except Exception as e:
       print("Oeps an Error")
       print(f"NOT OK: {str(e)}")
       return 0


def SunControl(id, Sun):
   #Sun = Sun Up and Down setting for function switch
   if Sun == "Up":
      EndLevel = 100 # preset Sun Up or max duty cycle
   elif Sun == "Down":
      EndLevel = 0   # preset Sun Down or min duty cycle

   #Lastlevel = id_name[id]["lastlevel"]  # 0 - 100 % | for test 90%
   ToGoLevel = abs(EndLevel - id_name[id]["lastlevel"]) # abs is used for creating positive value
   ToGoTime = id_name[id]["TimeEnd"] - datetime.now()
   #ActionTimeDelta = ToGoTime.total_seconds() / ToGoLevel
   if ToGoLevel > 0 and ToGoLevel <= 100:  # prevent dev by zero and end of function
      ActionTimeDelta = ToGoTime.total_seconds() / ToGoLevel   # Action Steps in seconds to take
      #print("ActionTimeDelta : " + str(ActionTimeDelta) + "  Type = " + str(type(ActionTimeDelta)))
      if id_name[id]["TimeNextAction"] == '':   # fistrun fill 
         id_name[id]["TimeNextAction"] = datetime.now() + timedelta(seconds=ActionTimeDelta) # for first loop
         print("---=== hit first run ===---")
      elif id_name[id]["TimeNextAction"] <= datetime.now():
         if Sun == "Up":
            id_name[id]["lastlevel"] += 1
         elif Sun == "Down":
            id_name[id]["lastlevel"] -= 1
         print(str(id) + " : " + str(id_name[id]["lastlevel"]) + " Action : " + str(id_name[id]["TimeNextAction"]))
         id_name[id]["TimeNextAction"] = datetime.now() + timedelta(seconds=ActionTimeDelta)
         return id_name[id]["lastlevel"]   # return value extra option for implementation
   else:
      id_name[id]["TimeEnd"] = ''
      return EndLevel
      #print("---=== End of function ===---")
      #quit() # quit at this point



if __name__ == '__main__':
  # Script has been called directly

  # Dictionary of switches to process, the key is for debuging
  # for reference see cli raspberry pi pinout command for "pin"
  # "Label" {"domotiz_idx", "domoticz_lastupdate", "domoticz_lastlevel", "TimeNextAction level change", "TimeDelay in min", "TimeEnd function", "pin gpio"} 
  id_name = {"JMB-C1":      {"idx" : 7297, "lastupdate" : '', "lastlevel" : '', "DeviceState" : '', "changed" : 1, "TimeNextAction" : '', "TimeDelay" : 1, "TimeEnd" : '', "pin" : 12, "LastupdateLocal" : '' },
             "JMB-C2":      {"idx" : 7298, "lastupdate" : '', "lastlevel" : '', "DeviceState" : '', "changed" : 1, "TimeNextAction" : '', "TimeDelay" : 1, "TimeEnd" : '', "pin" : 13, "LastupdateLocal" : '' },
             "JMB-C3":      {"idx" : 7299, "lastupdate" : '', "lastlevel" : '', "DeviceState" : '', "changed" : 1, "TimeNextAction" : '', "TimeDelay" : 1, "TimeEnd" : '', "pin" : 18, "LastupdateLocal" : '' },
             "JMB-C4":      {"idx" : 7300, "lastupdate" : '', "lastlevel" : '', "DeviceState" : '', "changed" : 1, "TimeNextAction" : '', "TimeDelay" : 1, "TimeEnd" : '', "pin" : 19, "LastupdateLocal" : '' },
             "JMB-C5":      {"idx" : 7301, "lastupdate" : '', "lastlevel" : '', "DeviceState" : '', "changed" : 1, "TimeNextAction" : '', "TimeDelay" : 1, "TimeEnd" : '', "pin" :  4, "LastupdateLocal" : '' },
             "JMB-SunUp":   {"idx" : 7304, "lastupdate" : '', "lastlevel" : '', "DeviceState" : '', "changed" : 1, "TimeNextAction" : '', "TimeDelay" : 1, "TimeEnd" : '', "SunDirection" : '', "LastupdateLocal" : ''},
             "JMB-SunDown": {"idx" : 7305, "lastupdate" : '', "lastlevel" : '', "DeviceState" : '', "changed" : 1, "TimeNextAction" : '', "TimeDelay" : 1, "TimeEnd" : '', "SunDirection" : '', "LastupdateLocal" : ''}}
  # fill Dict with datetime and startsetup
  for key in sorted(id_name):
     id_name[key]["lastupdate"] = datetime.now()
     #id_name[key]["LastupdateLocal"] = datetime.now()
     id_name[key]["lastlevel"] = 0  # first run setup
  # sort keys, then get values from original - fast
  id_name = {k: id_name[k] for k in sorted(id_name)}
  # end fill and sort Dict
  firststart = datetime.now()
  try:
     while True:
        for key in sorted(id_name):
           if key.startswith("JMB-C"):
              UpdatePWM(key, getSetting(key))
              if id_name[key]["TimeEnd"] != '':   # if not ended start function
                 SunValue = SunControl(key, id_name["JMB-SunUp"]["SunDirection"])
                 PushSetting(id_name[key]["idx"], SunValue)
           elif key.startswith("JMB-SunU"):
              SunDirection = getSetting(key)
              # function buttonpress
              DeltaFirstRun = datetime.now() - firststart
              #print(str(DeltaFirstRun.total_seconds()))
              if DeltaFirstRun.total_seconds() <= 2:
                 print("---=== First Run keep " + str(key) + " off ===---")
                 id_name[key]["changed"] = 0
              if id_name[key]["DeviceState"] == "On" and id_name[key]["changed"] == 1:
                 id_name[key]["SunDirection"] = "Up"
                 for subkey in sorted(id_name):
                    id_name[subkey]["TimeEnd"] = datetime.now() + timedelta(minutes=id_name[subkey]["TimeDelay"])  # at buttonpress set TimeEnd to finish
              elif id_name[key]["DeviceState"] == "Off" and id_name[key]["changed"] == 1:
                 id_name[key]["SunDirection"] = "Down"
                 for subkey in sorted(id_name):
                    id_name[subkey]["TimeEnd"] = datetime.now() + timedelta(minutes=id_name[subkey]["TimeDelay"])  # at buttonpress set TimeEnd to finish
           time.sleep(0.1)
  except KeyboardInterrupt:
     pi.stop() # Cleans the GPIO and Disconnect from local Pi
     print(" --== ByeBye ==-- ")
