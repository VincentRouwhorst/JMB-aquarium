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
import json
import chardet

DOMOTICZ_IP = 'http://127.0.0.1:8080'

def getSetting(id):
   try:
       #print(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(id))
       r = requests.get(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(id))
       siteresponse = r.json()
       if (r.ok): # response check is ok
          DeviceLevel = int(siteresponse['result'][0]['Level'])
          #print(DeviceLevel)
          DeviceState = siteresponse['result'][0]['Data']
          #print(DeviceState)
          if DeviceState == "Off":
            return 0
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
   print(DOMOTICZ_IP + "/json.htm?type=command&param=switchlight&idx=" + str(id) + "&switchcmd=Set%20Level&level=" + str(leveltoset))
   r = requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=switchlight&idx=" + str(id) + "&switchcmd=Set%20Level&level=" + str(leveltoset))
   siteresponse = r.json()
   if (r.ok): # response check is ok
      print("OK")
      #DeviceLevel = int(siteresponse['result'][0]['Level'])
      #print(DeviceLevel)
      #DeviceState = siteresponse['result'][0]['Data']
      #print(DeviceState)
      #if DeviceState == "Off":
      #  return 0
      #elif DeviceLevel >= 0 and DeviceLevel <= 100: # Extra safety levels must be between 0 and 100
      #  return DeviceLevel
      #else:
      #  return 0
   #else: # response check failed
      #return 0


if __name__ == '__main__':
  # Script has been called directly

  # Dictionary of switches to process, the key is for debuging
  id_name = {"JMB-C1": 7297, "JMB-C2": 7298, "JMB-C3": 7299, "JMB-C4": 7300, "JMB-C5": 7301}
  
  for key in sorted(id_name):
     print(key)
     print(getSetting(id_name[key]))
  PushSetting(7297, 50)
  ########### Work in progress ############
#while True:
