import sys
import base64
import struct
import datetime
import math
import dateutil.parser

str_format="%Y-%m-%dT%H:%M:%S.%f"
myfile = sys.argv[1]
index = 0 
for line in open(myfile, 'r'):
    comp_time, base64s = line.split(',')
    comp_datetime =  dateutil.parser.parse(comp_time)
    binary = base64.b64decode(base64s)
    fmt = '<BIHBBBBBI'
    #print struct.calcsize(fmt)
    #print(binary)
    #print(type(binary))
    #print(len(binary))
    state_data = struct.unpack(fmt, binary)
    seconds = state_data[7] + state_data[8] / 1000000000.0
    second_int = int(math.floor(seconds))
    microseconds = int((seconds - second_int) * 1000000.0)
    index+=1;
    try:
        utc_time = datetime.datetime(state_data[2], state_data[3], state_data[4], state_data[5], 
                                     state_data[6], second_int, microseconds, comp_datetime.tzinfo)
        print("{0},{1},{2},{3},{4}".format(index, comp_time, comp_datetime.strftime(str_format), utc_time.strftime(str_format), (comp_datetime - utc_time)))
    except ValueError:
        continue

