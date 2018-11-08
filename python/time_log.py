import sys
import base64
import struct
import datetime
import math
import dateutil.parser

str_format="%Y-%m-%dT%H:%M:%S.%f"
myfile = sys.argv[1]
index = 0 
firsttime = 0
for line in open(myfile, 'r'):
    comp_time, base64s = line.split(',')
    comp_time = comp_time.replace("\"", "")
    base64s = base64s.replace("\"", "")
    comp_datetime =  dateutil.parser.parse(comp_time)
    if index == 0:
        first_time = comp_datetime
    elapsed_time = comp_datetime - first_time
    binary = base64.b64decode(base64s)
    log_level = ord(binary[0])
    index+=1
    try:
        print("{0},{1},{2},{3},\"{4}\"".format(index, elapsed_time, comp_time, log_level, binary[1:]))
    except ValueError:
        continue

