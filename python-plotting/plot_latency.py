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

def hdf5ify(filename):
  import sys
  my_env = os.environ
  my_env['DYLD_LIBRARY_PATH'] = "/Users/dzollo/source/gnss-analysis/libswiftnav-private/build/install/usr/local/lib"

  my_env['LD_LIBRARY_PATH'] = "/Users/dzollo/source/gnss-analysis/libswiftnav-private/build/install/usr/local/lib"
  sys.path.append("PATH=~/miniconda2/bin:$PATH")
  cmd_string = ['export DYLD_LIBRARY_PATH="/Users/dzollo/source/gnss-analysis/libswiftnav-private/build/install/usr/local/lib" && source ~/miniconda2/bin/activate gnss_analysis && python ~/source/gnss-analysis/gnss_analysis/tools/sbp2hdf5.py', filename ]
  print cmd_string
  if not os.path.isfile(filename + ".hdf5"):
    os.system(" ".join(cmd_string)) 

def add_lines(events, vert):
  legend = []
  for each in events.itertuples():
    plt.plot([each[1], each[1] + datetime.timedelta(0, 0.001)], [0,vert] )
    legend.append(each[2])
  return legend

def plot(events, df, cycle, outdir=''):
  print df
  import numpy as np
  import dateutil.parser
  track = df['trackingstate_rover']
  rover_obs = df['rover']
    
  plt.figure(figsize=[20,20])
  l1s = rover_obs[rover_obs['band']=='1']
  l2s = rover_obs[rover_obs['band']=='2']
  for each in track.columns:
    #print each
    pass
  plt.subplot(3,1,1)

  plt.title("tracking state CN0s")
  legend = add_lines(events, 64)
  for i in range(64):
    try:
      cn0s = track['states_' + str(i) + "_cn0"]
      if (cn0s != 0).any():
        masked_time = track[cn0s != 0]['host_time']
        masked_CN0 = track[cn0s != 0]['states_' + str(i) + '_cn0']
        #print track['states_' + str(i) + '_sid_sat'].describe()
        plt.plot(masked_time, masked_CN0/4.0, 'x')
    except KeyError:
      #print i
      pass
  plt.legend(legend)
  plt.subplot(3,1,2)
  plt.title("obs CN0s")
  labels = add_lines(events, 64)
  for label, series in l1s.groupby('sid'):
    plt.plot(series['host_time'], series['carrier_noise_ratio'], 'x')
    labels.append(label)
  plt.legend(labels)
  plt.subplot(3,1,3)
  labels = labels = add_lines(events, 14)
  valid_l2s = l2s[l2s['raw_pseudorange'] != np.nan].groupby('host_time')
  plt.plot(valid_l2s['host_time'].agg(['max']), valid_l2s['sat'].agg(['count']))
  valid_l1s = l1s[l1s['raw_pseudorange'] != np.nan].groupby('host_time')
  plt.plot(valid_l1s['host_time'].agg(['max']), valid_l1s['sat'].agg(['count']))
  llh = df['piksi_absolute_llh']
  llh = llh[llh['fix_mode'] != 0]
  plt.plot(llh['host_time'], llh['n_sats'])
  time_array = []
  num_sat_array = []
  for each in track.groupby('host_time'):
    time_array.append(each[0])
    sat_list = []
    #print each
    for i in range(64):
      try:
        cn0s = each[1]['states_' + str(i) + "_cn0"]
        if (cn0s != 0).any():
          #print each[1]['states_' + str(i) + "sid_code"]
          #print each[1]['states_' + str(i) + "sid_sat"]
          sat_list.append(str(each[1]['states_' + str(i) + "_sid_code"]) + str(each[1]['states_' + str(i) + "_sid_sat"]))
      except KeyError:
        #print i
        pass
    new_list = []
    for i in sat_list:
      if i not in new_list:
        new_list.append(i)
    num_sat_array.append(len(new_list))

  plt.plot(time_array, num_sat_array)
  plt.legend(labels + ["num l2 code obs", "num l1 code obs", 'llh_n_sats', 'trk_num_sats'])
  plt.savefig(os.path.join(outdir, str(cycle) + ".png"))


def plot_error(events, df, nav_cycledf, cycle, outdir=''):
  plt.figure(figsize=[20,20])
  plt.subplot(2,1,1)
  labels = add_lines(events, max(nav_cycledf['EHPE [m]'].max() ,nav_cycledf['2D Error [m]'].max() ))
  print nav_cycledf.columns
  plt.plot(nav_cycledf['UTC'], nav_cycledf['EHPE [m]'])
  plt.plot(nav_cycledf['UTC'], nav_cycledf['2D Error [m]'])
  plt.legend(labels + ["EPEH [M]", '2D Error [m]'])
  plt.subplot(2,1,2)
  labels = add_lines(events, 5)
  plt.title("Fix mode")
  plt.plot(nav_cycledf['UTC'], nav_cycledf['Fix Mode'])
  plt.savefig(os.path.join(outdir, str(cycle) + "error.png"))


def setup(inpath, cycle, nav_df, event_df):
  events = event_df[event_df['cycle']==cycle]
  event_len = len(events) - 1
  start_time_pc = events.iloc[0]['host_time']
  end_time_pc = events.iloc[event_len]['host_time']
  outpath = os.path.join(inpath, "raw")
  outfile = select_from_json(inpath, outpath, cycle, start_time_pc, end_time_pc)
  hdf5ify(outfile)
  if os.path.isfile(outfile + '.hdf5'):
    dfcycle = pd.HDFStore(outfile + '.hdf5')
    return (events, dfcycle, nav_df[nav_df.index==cycle])
  else:
    return (None, None, None)



#outdir = '/tmpdata/rf-on-off/LJ23/20170925-174559-lj23-t2-d12h-f1-SPS-RFOnOff-1-5s'
#outdir = '/Volumes/data/data/PiksiMultiTesting/2017-09/28-corr-on-off-obs-view/LJ22/20170928-141412-lj22-t6-d60m-f3-RTK-CorrOnOff-1m/'
#indir = '/Volumes/data/data/PiksiMultiTesting/2017-09/27-v1.2.5-initial-test-GLO-10hz/LJ13/20170927-152912-lj13-t3-d24h-f4-RTK-Starts/'
indir = '/Users/dzollo/testdata/20180515-184456-lj23-t3-d6h-f4-RTK-Starts/'
outdir = os.path.join(indir, "figures")
if not os.path.isdir(outdir):
  os.mkdir(outdir)
for cycle in range(1, 5):
  event_df = pd.DataFrame(pp_gtt_events(indir))
  nav_df = getnav(indir)
  (events, df, navcycledf) = setup(indir, cycle, nav_df, event_df)
  plot_error(events, df, navcycledf, cycle, outdir)
  plot(events,df, cycle, outdir)
#for cycle in range(1,1000):
#  (events, df) = setup(outdir, cycle, event_df)
#  plot(events,df,cycle,outdir)

