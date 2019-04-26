import sys
import os
import json
from pprint import pprint
from sbp.navigation import MsgPosLLH, MsgVelNED
import math

def main():
  filepath = sys.argv[1]

  if not os.path.isfile(filepath):
    print("File path {} does not exist. Exiting...".format(filepath))
    sys.exit()
  

  with open(filepath) as sbp_post:
    outfile = open(filepath.split(".")[0]+"_conv.sbp.json",'w')
        # first, seek to earliest time of week that is the same
    for json_text_line in sbp_post:
      if json_text_line.startswith('{') and json_text_line.endswith('}\n'):
        current_msg = json.loads(json_text_line)
        if (current_msg is not None):
          tow = current_msg.get("data").get("obs_time")

          #print current_msg
          print(tow)
          #msg = MsgPosLLH(**extra_msg)
          #outfile.write(msg.to_json())
          #outfile.write(json_text_line)

  outfile.close()

if __name__ == '__main__':
  main()
