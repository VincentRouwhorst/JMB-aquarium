#!/usr/bin/python

from datetime import datetime

id_name = {"JMB-C1": {"idx" : 7297, "lastupdate" : ''}, "JMB-C2": 7298, "JMB-C3": 7299, "JMB-C4": 7300, "JMB-C5": 7301}
#dict = {'device': 'JMB-1', 'age': 26}

print(id_name["JMB-C1"]["idx"])

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
