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

  msg_gaps = []
  start_current_gap = None
  end_current_gap = None
  prev_tow = None

  count_blank_tow = 0

  with open(filepath) as sbp_json:
    for json_text_line in sbp_json:
      current_msg = None
      if json_text_line.startswith('{') and json_text_line.endswith('}\n'):
        current_msg = json.loads(json_text_line)
      if (current_msg is not None):
        msg_type = current_msg.get('msg_type')
        if msg_type == 522:
          current_tow = current_msg.get('tow')
          if current_tow == 0:
            count_blank_tow = count_blank_tow + 1
            if prev_tow is not None and prev_tow != 0:
              start_current_gap = prev_tow
          elif current_tow != 0 and prev_tow == 0 and start_current_gap is not None:
            end_current_gap = current_tow
            new_gap = {'start': start_current_gap,
                      'end': end_current_gap}
            pprint(new_gap)
            msg_gaps.append(new_gap)
            start_current_gap = None
            end_current_gap = None
          prev_tow = current_tow
  print(msg_gaps)

  outfile = open(filepath.split(".")[0]+"_conv.sbp.json",'w')

  current_gap_idx = 0
  removed_count = 0
  with open(filepath) as sbp_json:
    for json_text_line in sbp_json:
      current_msg = None
      extra_msg = None
      if json_text_line.startswith('{') and json_text_line.endswith('}\n'):
        current_msg = json.loads(json_text_line)
      if (current_msg is not None):
        msg_type = current_msg.get('msg_type')
        if msg_type == 529:
          current_tow = current_msg.get('tow')
          try:
            current_gap = msg_gaps[current_gap_idx]
            start = current_gap.get('start')
            end = current_gap.get('end')
            if start <= current_tow <= end:
              current_msg['flags']=13
            if current_tow > end:
              current_gap_idx = current_gap_idx + 1
          except IndexError:
            pass
          outfile.write(json.dumps(current_msg)+'\n')
          extra_msg = current_msg.copy()
          h_accuracy = math.sqrt(float(extra_msg['cov_n_n']) +  float(extra_msg['cov_e_e'])) * 1000
          v_accuracy = math.sqrt(float(extra_msg['cov_d_d'])) * 1000
          extra_msg['h_accuracy'] = int(h_accuracy)
          extra_msg['v_accuracy'] = int(v_accuracy)
          extra_msg.pop('cov_n_n')
          extra_msg.pop('cov_n_e')
          extra_msg.pop('cov_n_d')
          extra_msg.pop('cov_e_e')
          extra_msg.pop('cov_e_d')
          extra_msg.pop('cov_d_d')
          extra_msg['msg_type'] = 522
          msg = MsgPosLLH(**extra_msg)
          outfile.write(msg.to_json())
        elif msg_type == 530:
          current_tow = current_msg.get('tow')
          try:
            current_gap = msg_gaps[current_gap_idx]
            start = current_gap.get('start')
            end = current_gap.get('end')
            if start <= current_tow <= end:
              current_msg['flags']=11
          except IndexError:
            pass
          outfile.write(json.dumps(current_msg)+'\n')
          extra_msg = current_msg.copy()
          h_accuracy = math.sqrt(extra_msg['cov_n_n'] +  extra_msg['cov_e_e'])
          v_accuracy = math.sqrt(extra_msg['cov_d_d'])
          extra_msg['h_accuracy'] = h_accuracy
          extra_msg['v_accuracy'] = v_accuracy
          extra_msg.pop('cov_n_n')
          extra_msg.pop('cov_n_e')
          extra_msg.pop('cov_n_d')
          extra_msg.pop('cov_e_e')
          extra_msg.pop('cov_e_d')
          extra_msg.pop('cov_d_d')
          extra_msg['msg_type'] = 526
          msg = MsgVelNED(**extra_msg)
          outfile.write(msg.to_json())
        elif msg_type == 522:
          current_tow = current_msg.get('tow')
          if (current_tow == 0):
            removed_count = removed_count + 1
          else: # we should have already written an equivalent
            # outfile.write(json.dumps(current_msg)+'\n')
            pass
        elif msg_type == 526:
          current_tow = current_msg.get('tow')
          if (current_tow == 0):
            removed_count = removed_count + 1
          else: # we should have already written an equivalent
            #outfile.write(json.dumps(current_msg)+'\n')
            pass
        else:
          outfile.write(json_text_line)

  outfile.close()
  print 'removed_count: %d' % removed_count
  print 'count_blank_tow: %d' % count_blank_tow

if __name__ == '__main__':
  main()
