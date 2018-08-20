import sys
import base64
import struct
import datetime
import math
import dateutil.parser

str_format="%Y-%m-%d %H:%M:%S.%f"
myfile = sys.argv[1]
index = 0 
firsttime = 0
for line in open(myfile, 'r'):
    comp_time = line[0:26]
    msg = line[26:-1]
    comp_time = comp_time.replace("[", "").replace("]","")
    #print(comp_time)
    comp_datetime =  dateutil.parser.parse(comp_time)
    if index == 0:
        first_time = comp_datetime
    elapsed_time = comp_datetime - first_time
    index += 1
    try:
        print("{0},{1},{2},\"{3}\"".format(index, elapsed_time.total_seconds(), comp_datetime, msg.replace("\n","").replace("\r","")))
    except ValueError:
        continue

