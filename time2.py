import time
from datetime import datetime, timedelta

# Dictionary of switches to process, the key is for debuging
id_name = {"JMB-C1":      {"idx" : 7297, "lastupdate" : '', "lastlevel" : '', "TimeNextAction" : '', "pin" : 18},
           "JMB-C2":      {"idx" : 7298, "lastupdate" : '', "lastlevel" : '', "TimeNextAction" : '', "pin" : 32 },
           "JMB-C3":      {"idx" : 7299, "lastupdate" : '', "lastlevel" : '', "TimeNextAction" : '', "pin" : 32 },
           "JMB-C4":      {"idx" : 7300, "lastupdate" : '', "lastlevel" : '', "TimeNextAction" : '', "pin" : 32 },
           "JMB-C5":      {"idx" : 7301, "lastupdate" : '', "lastlevel" : '', "TimeNextAction" : '', "pin" : 32 },
           "JMB-SunUp":   {"idx" : 7304, "lastupdate" : '', "lastlevel" : '', "TimeNextAction" : '', "pin" : 32 },
           "JMB-SunDown": {"idx" : 7305, "lastupdate" : '', "lastlevel" : '', "TimeNextAction" : '', "pin" : 32 }}

for key in sorted(id_name):
   id_name[key]["lastupdate"] = datetime.now()
   id_name[key]["lastlevel"] = 10  # test setup

# ---=== SunControl ===---
# T1 = starttime datetime.now()
# T2 = endtime
# T1 ------A ------A -------A --------A -------A T2
# Tnow------------------------------Tnow-------Tnow
# T2 = Tnow + Tdelta
#
# SunUp and SunDown
# StartLevel----A ------A -----A -----A ------EndLevel
# 0-----1------1-----1-----1-----1-----1---- 100
# 0--------------------45--------------------100
#
# ToGoLevel = EndLevel - lastlevel
#     55   =      100 - 45
#
# ToGoTime = T2 - Tnow
#
# TimeNextAction = ToGoTime / ToGoLevel
#  1,636363636363636  = 90 / 55

T1 = datetime.now()
T2 = T1 + timedelta(minutes=1)   # at buttonpress settime to finish

def SunControl(id, Sun):
   global T2
   #Sun = Sun Up and Down setting for function switch
   if Sun == "Up":
      EndLevel = 100 # preset Sun Up
   elif Sun == "Down":
      EndLevel = 0   # preset Sun Down

   #Lastlevel = id_name[id]["lastlevel"]  # 0 - 100 % | for test 90%
   ToGoLevel = abs(EndLevel - id_name[id]["lastlevel"]) # abs is used for creating positive value
   ToGoTime = T2 - datetime.now()
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
      print("---=== End of function ===---")
      quit() # quit at this point


while True:
 for key in sorted(id_name):
    SunControl(key, "Down")
