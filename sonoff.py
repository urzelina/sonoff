#!/usr/bin/python3

# /usr/local/bin/sonoff.py
# use sys arguments   -> sonoff.py device-name action(on|off)
# Copyright C 2020  aPeer.nl   


import requests
import sys
import json
from datetime import datetime


# sonoff1 is buitenlamp bij poort
# sonoff2 is stekker doos computer geert
# sonoff3 is raamspotjes keuken kamer
# sonoff4 
device_dict =   {
                    'sonoff1': ("10.42.65.171","1000b68daf","D8-F1-5B-E0-7B-0E"),# 		demen buitenlamp bij poort
                    'sonoff2': ("10.42.65.172","1000c973e6","60-01-94-FD-8E-99"),# 		demen stekker doos computer geert
                    'sonoff3': ("10.42.65.173","10009083aa","DC-4F-22-A6-4E-CD"),# 		demen raamspotjes keuken kamer
                    'sonoff4': ("10.42.65.174","100090ed81","C4-4F-33-B3-23-88"),
                    'sonoff5': ("10.42.11.175","1000c8ff6d","60-01-94-E5-6F-F1"),#		urzelina outdoor light cabana
                    'sonoff6': ("10.42.65.176","1000c8e5c8","60-01-94-FD-8C-BD"),
                    'sonoff7': ("10.42.11.177","","D8-F1-5B-C5-C2-B4"),# 			urzelina fan cabana
                    'sonoff8': ("10.42.11.178","","D8-F1-5B-C5-BE-59")#    			urzelina outdoor lights cocheira
                }


def write_to_log(logdata):
    timest = datetime.now().strftime("%d/%m/%Y--%H:%M:%S => ")
    try:
        with open("/var/log/sonoff.log", "a") as f:
            f.write("%s %s \n" % (timest, logdata))
    except:
        pass
write_to_log("Start %s %s"  % (sys.argv[1],sys.argv[2]))

def rest_api(api_url, api_device, api_action):
    requesturl = "http://" + api_url + ":8081/zeroconf/switch"
    headers = {'Content-type': 'application/json', }
    data1 = json.dumps({'deviceid': api_device, 'data': {'switch': api_action}})
    try:
        response = requests.post(requesturl, headers=headers, data=data1, timeout=5)
    except:
        pass
    try:
        chkvalue = response.status_code == requests.codes.ok
    except:
        chkvalue = False
        write_to_log("device with ip %s is not responding" % requesturl)
    if chkvalue:
        write_to_log(response.status_code)


rest_api(device_dict[sys.argv[1]][0],device_dict[sys.argv[1]][1],sys.argv[2])



