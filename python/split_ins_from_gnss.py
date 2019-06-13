#!/usr/local/bin/python3
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
      gnss_out = ".".join(filepath.split(".")[0:-2]) + ".gps.sbp.json"
      print("gnss output to  {}".format(gnss_out))
      ins_out = ".".join(filepath.split(".")[0:-2])+".ins.sbp.json"
      print("ins output to  {}".format(ins_out))
      outfile_gnss = open(gnss_out, 'w')
      outfile_ins = open(ins_out, 'w')

      with open(filepath, 'r') as sbp_json:
        for i, json_text_line in enumerate(sbp_json):
          current_msg = None
          if json_text_line.startswith('{'):
              try:
                  current_msg = json.loads(json_text_line)
                  msg_type = current_msg.get('msg_type', None)
              except AttributeError as e:
                  print("attribute error at line {} : {}".format(i, e))
                  print("text was: {}".format(json_text_line))
          else:
              print("error, no json for line index {}: {}".format(i, json_text_line))
              continue
          if (current_msg is not None):
              if msg_type is not None:
                  if msg_type in MSGS_TO_FILTER:
                      flags = base64.b64decode(current_msg.get('payload'))[-1]
                      flags = base64.b64decode(current_msg.get('payload'))[-1]
                      #print("writing to one file")
                      if flags > 8:
                        outfile_ins.write(json_text_line + '\n')
                      else:
                        outfile_gnss.write(json_text_line + '\n')
                  else:
                      #print("writing to both files")
                      outfile_ins.write(json_text_line + '\n')
                      outfile_gnss.write(json_text_line + '\n')
              else:
                 print("error, no msg_type for line {}: {}".format(i, json_text_line))
                 continue
          else:
                print("error, json issue for line {}: {}".format(i, json_text_line))
                continue

      outfile_gnss.close()
      outfile_ins.close()

if __name__ == '__main__':
  main()
