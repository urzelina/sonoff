#!/usr/bin/python3





# '''
# /usr/local/bin/set_daily_sonoff_times.py
#
# local date on pi is Amsterdam


# cronjob every day at 11:01 to set on / off times (infile  /etc/cron.d/set_daily_sonoff_times) 
# created december 2018  Geert Sillekens 
# '''
import os
import time
from suntime import Sun         # pip3 install Suntime
from random import randint
from datetime import datetime
from datetime import timedelta
from dateutil import tz

def write_to_log(logdata):
    timest = datetime.now().strftime("%d/%m/%Y--%H:%M:%S => ")
    with open("/var/log/sonoff.log", "a") as f:
        f.write("%s %s \n" % (timest, logdata))
        

def utc2local(utc):      # convert utc time (from Sun) to local time zone time
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset
      

#  lon lat voor demen
coords = {'longitude' : 5.38, 'latitude' : 51.49 }
coords_urzelina = {'longitude' : -28.8, 'latitude' : 38.39 }
sun = Sun(coords['latitude'],coords['longitude'])


# Sunrise time UTC (decimal, 24 hour format)
# print(sun.getSunriseTime( coords ))

# Sunset time UTC (decimal, 24 hour format)



sunrise = utc2local(sun.get_sunrise_time())    # zonsopkomst geconverteerd naar local time zone
sunset = utc2local(sun.get_sunset_time())      # zonsondergang geconverteerd naar local time zone




print(sunrise)
print(sunset)


sunsethr = int(sunset.strftime('%H'))#           Europe/Amsterdam time!!
sunsetmin = int(sunset.strftime('%M'))

sunrisehr = int(sunrise.strftime('%H'))#         Europe/Amsterdam time!!
sunrisemin = int(sunrise.strftime('%M'))


 


offhr = 23
offmin = (randint(35, 57))





write_to_log("Settings daily sunset  %s:%s sunrise %s:%s " % (sunsethr, sunsetmin, sunrisehr, sunrisemin))


# buitenlamp oost gevel
with open("/etc/cron.d/sonoff1_on", "w")  as f:
  f.write("\n")
  f.write("%s %s * * * root /usr/local/bin/sonoff.py sonoff1 on" % (sunsetmin, sunsethr))
  f.write("\n")

with open("/etc/cron.d/sonoff1_off", "w")  as f:
  f.write("\n")
  f.write("%s %s * * * root /usr/local/bin/sonoff.py sonoff1 off" % (sunrisemin, sunrisehr))
  f.write("\n")
  
# plafond inbouw spots keuken/kamer sonoff3
with open("/etc/cron.d/sonoff3_on", "w")  as f:
  f.write("\n")
  f.write("%s %s * * * root /usr/local/bin/sonoff.py sonoff3 on" % (sunsetmin, sunsethr))
  f.write("\n")

with open("/etc/cron.d/sonoff3_off", "w")  as f:
  f.write("\n")
  f.write("%s %s * * * root /usr/local/bin/sonoff.py sonoff3 off" % (offmin, offhr))
  f.write("\n")

