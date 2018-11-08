#!/usr/local/bin/python2
import sys
import os
import json
import math
import base64

MSGS_TO_FILTER = [521, #MsgPosECEF
                  522, #MsgPosLLH
                  525, #MsgVelECEF
                  526, #MsgVelNED
                  529, #MsgPosLLHCov
                  530, #MsgVelNEDCov
                  532, #MsgPosECEFCov
                  533  #MsgVelECEFCov
                  ]

def main():
  for filepath in sys.argv[1:]:
      print("Processing filepath {}".format(filepath))
      if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

      outfile_gnss = open(filepath.split(".")[0]+".gps.sbp.json",'w')
      outfile_ins = open(filepath.split(".")[0]+".ins.sbp.json",'w')

      with open(filepath) as sbp_json:
        for json_text_line in sbp_json:
          current_msg = None
          if json_text_line.startswith('{'):
              current_msg = json.loads(json_text_line)
              if current_msg.get('data') != None:
                  current_msg = current_msg.get('data')
              msg_type = current_msg.get('msg_type')
          else:
              print("error, no json")
              sys.exit()
          if (current_msg is not None):
              if msg_type in MSGS_TO_FILTER:
                  flags = ord(base64.b64decode(current_msg.get('payload'))[-1])
                  if flags > 8:
                    outfile_ins.write(json.dumps(current_msg)+'\n')
                  else:
                    outfile_gnss.write(json.dumps(current_msg) + '\n')
              else:
                  outfile_ins.write(json.dumps(current_msg)+'\n')
                  outfile_gnss.write(json.dumps(current_msg) + '\n')
          else:
              print("error, no current_msg")
              sys.exit()
      outfile_gnss.close()
      outfile_ins.close()

if __name__ == '__main__':
  main()
