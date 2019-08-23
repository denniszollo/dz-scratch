import sys
import os
import json
from pprint import pprint
import math
from collections import defaultdict
MS_IN_WEEK = 7 * 24 * 60 * 60 * 1000
# go through a log and sort by time of week
# NOT ROBUST TO TOW ROLLOVER


def main():
  filepath = sys.argv[1]
  outfile = filepath.split(".")[0]+"_sort.sbp.json"
  if len(sys.argv) > 2:
      outfile = sys.argv[2]
  print("writing output to {}".format(outfile))
  if not os.path.isfile(filepath):
    print("File path {} does not exist. Exiting...".format(filepath))
    sys.exit()
  msg_window_size = 10000
  duration_to_retain_ms = 1000
  out_msg_tow_dict = defaultdict(list)
  last_tow_msg_id_dict = defaultdict(lambda: -1)
  week_elapsed_msg_id_dict = defaultdict(lambda: 0)
  last_tow = 0
  msg_counter = 0;
  elapsed_weeks = 0;
  with open(filepath) as sbp_json:
    with open(outfile, 'w') as out:
        for json_text_line in sbp_json:
          current_msg = None
          #print("json_text line is {}".format(json_text_line))
          if json_text_line[0] == '{' and json_text_line[-2] == '}':
            current_msg = json.loads(json_text_line)
            msg_id = current_msg.get("msg_type", "Unknown")
            current_tow = current_msg.get('tow', None)
            #print("current tow for msg {} is {}".format(msg_id, current_tow))
            if current_tow == None:
                current_tow = last_tow
                #print("setting tow to last valid tow  {}".format(last_tow))
            if current_tow < last_tow_msg_id_dict[msg_id]:
                week_elapsed_msg_id_dict[msg_id] += 1
                print("bumping weeknumber for msg {} to {}".format(
                    msg_id, week_elapsed_msg_id_dict[msg_id]))
            adjusted_tow = current_tow + week_elapsed_msg_id_dict[msg_id] * MS_IN_WEEK
            #if adjusted_tow != current_tow:
                #print("new tow is {}".format(adjusted_tow))
            out_msg_tow_dict[adjusted_tow].append(current_msg)
            last_tow = adjusted_tow
            msg_counter += 1
          else:
              print("json text didn't match {}".format(json_text_line))
          if msg_counter > msg_window_size:
              end_tow = last_tow - duration_to_retain_ms
              print("hit sorted output and will go up to {}".format(end_tow))
              for each_tow, msg_list in sorted(out_msg_tow_dict.items()):
                  if each_tow < end_tow:
                      print("outputting messages for tow {}.".format(each_tow))
                      while len(msg_list) !=0: 
                          each_msg = msg_list.pop()
                          #print("outputting {}".format(each_msg.get('msg_type', 'Unknown')))
                          out.write(json.dumps(each_msg, sort_keys=True) + '\n')
                          msg_counter -= 1
                      del out_msg_tow_dict[each_tow]
                          
        # end for each line in json
        for each_tow, msg_list in sorted(out_msg_tow_dict.items()):
            print("outputting messages for tow {} at end of script".format(each_tow))
            while len(msg_list) !=0: 
                each_msg = msg_list.pop()
                print("outputting {}".format(each_msg.get('msg_type', 'Unknown')))
                out.write(json.dumps(each_msg, sort_keys=True) + '\n')
            del out_msg_tow_dict[each_tow]
        for keys,values in out_msg_tow_dict.items():
            print(keys)
            print(values)


if __name__ == '__main__':
  main()
