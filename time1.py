#!/usr/bin/python

from datetime import datetime

id_name = {"JMB-C1":      {"idx" : 7297, "lastupdate" : '', "lastlevel" : ''}, 
             "JMB-C2":      {"idx" : 7298, "lastupdate" : '', "lastlevel" : ''}, 
             "JMB-C3":      {"idx" : 7299, "lastupdate" : '', "lastlevel" : ''}, 
             "JMB-C4":      {"idx" : 7300, "lastupdate" : '', "lastlevel" : ''}, 
             "JMB-C5":      {"idx" : 7301, "lastupdate" : '', "lastlevel" : ''}, 
             "JMB-SunUp":   {"idx" : 7304, "lastupdate" : '', "lastlevel" : ''}, 
             "JMB-SunDown": {"idx" : 7305, "lastupdate" : '', "lastlevel" : ''}}

print(id_name["JMB-C1"])

dt_string = "2022-01-02 20:54:10"
dt_string = dt_string.replace('-', '/')

id_name["JMB-C1"]["lastupdate"] = dt_string

print(">" + id_name["JMB-C1"]["lastupdate"])

dt_string2 = "2022-01-02 20:56:40"
dt_string2 = dt_string2.replace('-', '/')

# Considering date is in dd/mm/yyyy format
dt_object1 = datetime.strptime(dt_string, "%Y/%m/%d %H:%M:%S")
dt_object2 = datetime.strptime(dt_string2, "%Y/%m/%d %H:%M:%S")

print("dt_object1 =", dt_object1)
print("dt_object2 =", dt_object2)
delta = dt_object2 - dt_object1
print(delta)
#print(type(dt_object1))

# Considering date is in mm/dd/yyyy format
#dt_object2 = datetime.strptime(dt_string, "%m/%d/%Y %H:%M:%S")
#print("dt_object2 =", dt_object2)
