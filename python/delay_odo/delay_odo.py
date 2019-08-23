import sys
import os
import json
from pprint import pprint
from sbp.vehicle import MsgOdometry
import math

# go through a log and delay messages of type ODO by the provided number of milliseconds

def main():
  infilepath = sys.argv[1]
  offset = float(sys.argv[2])
  outfilepath = infilepath.split(".")[0]+"_delay_odo.sbp.json"
  if len(sys.argv) > 3:
      outfilepath = sys.argv[3]
  print("writing output to {}".format(outfilepath))
  delay_odo(infilepath, offset, outfilepath)

def delay_odo(filepath, offset, outfile):
  MS_IN_WEEK = 7 * 24 * 60 *60 * 1000
  print("here")
  if not os.path.isfile(filepath):
    print("File path {} does not exist. Exiting...".format(filepath))
    sys.exit()

  print("here2")
  msg_gaps = []
  start_current_gap = None
  end_current_gap = None
  prev_tow = None

  count_blank_tow = 0

  with open(filepath) as sbp_json:
    with open(outfile, 'w') as out:
        for json_text_line in sbp_json:
          current_msg = None
          #print("json line is {}".format(json_text_line))
          out_str = json_text_line
          if json_text_line.startswith('{') and json_text_line.endswith('}\n'):
            current_msg = json.loads(json_text_line)
            if (current_msg is not None):
              msg_type = current_msg.get('msg_type')
              if msg_type == 2307:
                current_tow = current_msg.get('tow')
                new_tow = current_tow + offset
                #print("delaying odo: formarlly {} now {}".format(current_tow, new_tow))
                if new_tow > MS_IN_WEEK:
                  new_tow -= MS_IN_WEEK
                if new_tow < 0:
                  new_tow += MS_IN_WEEK
                extra_msg = current_msg.copy()
                extra_msg['tow'] =  new_tow
                extra_msg.pop('payload')
                out_str = MsgOdometry(**extra_msg).to_json() + "\n"
              out.write(out_str)
          else:
              print("json doesn't match")

def make_list_of_id(infile, msg_id):
    outlist = []
    with open(infile) as sbp_json:
        for json_text_line in sbp_json:
          if json_text_line.startswith('{') and json_text_line.endswith('}\n'):
            current_msg = json.loads(json_text_line)
            if (current_msg is not None):
              msg_type = current_msg.get('msg_type')
              if msg_type == msg_id:
                  outlist.append(current_msg)
    return outlist


def test_end_to_end():
    infile = 'test_delay_odo.sbp.json'
    outfile = '/tmp/test.sbp.json'
    delay = -500.0
    delay_odo(infile, delay, outfile)
    # now iterate over each file and make a list of the dicts for each
    infile_odos =  make_list_of_id(infile, 2307)
    outfile_odos = make_list_of_id(outfile, 2307)

    for inodo, outodo in zip(infile_odos, outfile_odos):
        assert inodo['velocity'] == outodo ['velocity']
        timediff = outodo['tow'] - inodo['tow']
        assert abs(timediff - delay) < 1
    
if __name__ == '__main__':
  main()
