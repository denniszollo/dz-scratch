import sys
import struct
csvfile = sys.argv[1]
outfile = sys.argv[1] + ".nv.gps"


def hexstring_to_byte_array(hexstring):
    out = bytearray()
    retur

with open (csvfile, 'r') as inf:
    with open(outfile, 'wb') as out:
        for line in inf:
             if line.startswith('SpanMsgB'):
                   fields = line.split(",")
                   outbuffer = bytearray()
                   header = fields[8]
                   synch_string = 'AA4412'
                   if len(header) <= 24 :
                       synch_string = 'AA4413'
                   data = fields[10]
                   line = header + data
                   line = line.rstrip("\n")
                   #outstruct = struct.unpack('<' + str(len(line)/2) +'h', line)
                   #print line
                   outln = bytearray.fromhex(synch_string) + bytearray.fromhex(line) 
                   out.write(outln)

