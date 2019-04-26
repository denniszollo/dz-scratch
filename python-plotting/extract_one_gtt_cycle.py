import os
from collections import OrderedDict
import json
from datetime import datetime
import dateutil.parser
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

def pp_gtt_events(dut_path, sim_start_ts=None):
  '''
  Convert GTT event logs into HDF5.
  Parameters
  ----------
  iter_dir: str
    iteration directory path
  dut_name: str
    DUT name
  h5: pytables h5 file object
    HDF5 file
  sim_start_ts: datetime
    scenario start time, optional
  Returns
  -------
  datetime, scenario start time, optional
  '''
  file_path = os.path.join(dut_path, 'events.json')

  if not os.path.isfile(file_path):
    return None

  events = None
  with open(file_path) as f:
    config_data = json.load(f, object_pairs_hook=OrderedDict)
    events = []
    cycle = 1;
    for event in config_data['test_case']['events']:
      ts = dateutil.parser.parse(event['time'])
      if event['event'].startswith("Cycle"):
        cycle = event['event'].split(' ')[1]
      events.append((ts, event['event'], int(cycle)))
  if events:
    dtype =\
      ([('host_time', 'datetime64[ns]'),
        ('Event', 'S32'),
        ('cycle', 'int32')])

  gtt_events = None

  if events:
    gtt_events = np.array(events, dtype)
  if gtt_events is not None:
    return gtt_events
  else:
    return None


def select_from_json(inpath, path, cycle, start_time, end_time):
  if not os.path.isdir(path):
    os.mkdir(path)
  outfile = os.path.join(path, 'gnss-sbp-' + str(cycle) + '.sbp.json')
  cmd_string = ['cat', os.path.join(inpath, 'gnss-sbp.json'), '|', 'jq -c \'. | select(.time < ', 
                '\"' + str(end_time.isoformat()) + '\"', 'and .time  >', 
                '\"' + str(start_time.isoformat()) + '\"', ')\'']
  #cmd_string = ['jq -c \'. | select(.time < ', 
  #              '\"' + str(end_time.isoformat()) + '\"', 'and .time  >', 
  #              '\"' + str(start_time.isoformat()) + '\"', ')\'']
  cmd_string.append(">" + outfile)
  print " ".join(cmd_string)
  
  #try:
  #  with open(outfile, 'w') as out:
  #    #cat = subprocess.Popen(['cat', os.path.join(path, 'gnss-sbp.json')], stdout=subprocess.PIPE)
  #    jq = subprocess.check_call(cmd_string, stdout=out, shell=True)
  #except subprocess.CalledProcessError as e:
  #  print e.output
  #  print e.returncode
  #  print "error"
  #  return -1
  if not os.path.isfile(outfile):
    os.system(" ".join(cmd_string))
  return outfile 

def getnav(filename):
  return pd.DataFrame.from_csv(os.path.join(filename, 'nav.csv'))

def add_lines(events, vert):
  legend = []
  for each in events.itertuples():
    plt.plot([each[1], each[1] + datetime.timedelta(0, 0.001)], [0,vert] )
    legend.append(each[2])
  return legend


def setup(inpath, cycle, nav_df, event_df):
  events = event_df[event_df['cycle']==cycle]
  event_len = len(events) - 1
  start_time_pc = events.iloc[0]['host_time']
  end_time_pc = events.iloc[event_len]['host_time']
  outpath = os.path.join(inpath, "raw")
  outfile = select_from_json(inpath, outpath, cycle, start_time_pc, end_time_pc)
  if os.path.isfile(outfile + '.hdf5'):
    dfcycle = pd.HDFStore(outfile + '.hdf5')
    return (events, dfcycle, nav_df[nav_df.index==cycle])
  else:
    return (None, None, None)



indir = '/Volumes/data/data/DuroInertialTesting/2018-09/14-gt1-a-rtk-b-sbas-starts-v211-Ant-A5/DUT13/20180914-010733-lj13-t3-d12h-f6-SBAS-Starts/'
indir = '/Volumes/data/data/DuroInertialTesting/2018-09/14-gt1-a-rtk-b-sbas-starts-v211-Ant-A5/DUT12/20180914-010728-lj12-t3-d12h-f4-RTK-Starts/'
for cycle in [1,2]:
  event_df = pd.DataFrame(pp_gtt_events(indir))
  nav_df = getnav(indir)
  (events, df, navcycledf) = setup(indir, cycle, nav_df, event_df)

