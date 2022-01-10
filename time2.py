import time
from datetime import datetime, timedelta

def time_counter(seconds):
    starttime = time.time()
    while True:
        now = time.time()
        if now > starttime + seconds:
            break
        yield now - starttime


# Dictionary of switches to process, the key is for debuging
id_name = {"JMB-C1":      {"idx" : 7297, "lastupdate" : '', "lastlevel" : '', "changed" : 1, "pin" : 18},
           "JMB-C2":      {"idx" : 7298, "lastupdate" : '', "lastlevel" : '', "changed" : 1, "pin" : 32 },
           "JMB-C3":      {"idx" : 7299, "lastupdate" : '', "lastlevel" : '', "changed" : 1, "pin" : 32 },
           "JMB-C4":      {"idx" : 7300, "lastupdate" : '', "lastlevel" : '', "changed" : 1, "pin" : 32 },
           "JMB-C5":      {"idx" : 7301, "lastupdate" : '', "lastlevel" : '', "changed" : 1, "pin" : 32 },
           "JMB-SunUp":   {"idx" : 7304, "lastupdate" : '', "lastlevel" : '', "changed" : 1, "pin" : 32 },
           "JMB-SunDown": {"idx" : 7305, "lastupdate" : '', "lastlevel" : '', "changed" : 1, "pin" : 32 }}

#for key in sorted(id_name):
#   id_name[key]["lastupdate"] = datetime.now()

#Delta time is true eg 15 min
#starttime  
#endtime = starttime + countdowntime 
#countdowntimer = 900 # 15 min = 900 sec
#lamplevel = 100 # 0-10
#time.sleep(countdowntimer/lamplevel) #step to take action

#T1 = starttime
#T2 = endtime
#T1 ------A ------A -------A --------A -------A T2
#Tnow------------------------------Tnow-------Tnow
#T2 = Tnow + Tdelta

#SunUp and SunDown
#StartLevel----A ------A -----A -----A ------EndLevel
#0-----1------1-----1-----1-----1-----1---- 100
#0--------------------45--------------------100

#togolevel = EndLevel - lastlevel
#     55   =      100 - 45

#togotime = T2 - Tnow

#actiontimedelta = togotime/ togolevel
#  1,636363636363636  = 90 / 55

#TimeNextAction = Tnow + actiontimedelta

# Exact TAction is extream rare so
#if TAction >= Tnow:
#   if lastlevel => 0 and <= 100:
#     LastLevel -1   result must be int()

#for t in time_counter(5):
#    print(t)
#    time.sleep(1)

T1 = datetime.now()
T2 = T1 + timedelta(minutes=1)

#print(T1)
#print(T2)

Sun = "Down"   # Sun Up and Down setting for function switch
EndLevel = 0   # preset if Sun Up Down
Lastlevel = 100
ToGoLevel = abs(EndLevel - Lastlevel) # abs is used for creating positive value
ToGoTime = T2 - datetime.now()
ActionTimeDelta = ToGoTime.total_seconds() / ToGoLevel
print(ActionTimeDelta)
#print("ActionTimeDelta : " + str(ActionTimeDelta) + "  Type = " + str(type(ActionTimeDelta)))
TimeNextAction = datetime.now() + timedelta(seconds=ActionTimeDelta) # for first loop
loopcount = 0 # set counter for loop

while True:
   ToGoLevel = abs(EndLevel - Lastlevel) # abs is used for creating positive value
   ToGoTime = T2 - datetime.now() # aftellen
   if ToGoLevel > 0 and ToGoLevel <= 100:  # prevent dev by zero and end of function
      ActionTimeDelta = ToGoTime.total_seconds() / ToGoLevel   # Action Steps in seconds to take
   else:
      print("---=== End of function ===---")
      break
   if TimeNextAction <= datetime.now():
      loopcount += 1
      if Sun == "Up":
         Lastlevel += 1
      elif Sun == "Down":
         Lastlevel -= 1
      print(str(Lastlevel) + " " + str(loopcount) + " Action : " + str(TimeNextAction) + " Now : " + str(datetime.now()))
      #time.sleep(0.5)
      TimeNextAction = datetime.now() + timedelta(seconds=ActionTimeDelta)
