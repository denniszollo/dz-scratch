import sys
import os
import json
from pprint import pprint
from sbp.navigation import MsgPosLLH, MsgVelNED
import math
                  
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
  filepath = sys.argv[1]

  if not os.path.isfile(filepath):
    print("File path {} does not exist. Exiting...".format(filepath))
    sys.exit()

  msg_gaps = []
  start_current_gap = None
  end_current_gap = None
  prev_tow = None

  count_blank_tow = 0

  outfile_ins = open(filepath.split(".")[0]+"_ins.sbp.json",'w')
  outfile_gnss = open(filepath.split(".")[0]+"_gnss.sbp.json",'w')

  with open(filepath) as sbp_json:
    for json_text_line in sbp_json:
      current_msg = None
      if json_text_line.startswith('{') and json_text_line.endswith('}\n'):
        current_msg = json.loads(json_text_line)
      if (current_msg is not None):
        msg_type = current_msg.get('msg_type')
        if msg_type in MSGS_TO_FILTER:
          flags = current_msg.get('flags')
          if ((flags & 0x8) >> 3) == 1: # ins used
            outfile_ins.write(json.dumps(current_msg) + "\n")
          else:
            outfile_gnss.write(json.dumps(current_msg) + "\n")
        else:
          outfile_ins.write(json.dumps(current_msg) + "\n")
          outfile_gnss.write(json.dumps(current_msg) + "\n")
      else:
        print("msg with string {} is none".format(json_text_line))

  outfile_ins.close()
  outfile_gnss.close()

if __name__ == '__main__':
  main()
