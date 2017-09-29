#!/usr/local/bin/python
import operator
import argparse
import os
import collections
import re
import platform
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 10000
PLOT_WIDTH = 16
PLOT_HEIGHT =12

# Column Naming conventions
ERR_COLUMNS = ['Error Info', 'Errors']
COMM_META_COL = ['Cycle', 'Start Time', 'Start UTC'] + ERR_COLUMNS 
CONT_META_COL = ['Msg Arrival Time [s]', 'TOW [s]']
REAQ_META_COL = ['Cycle Start', 'RF Off Time [s]', 'Nav Duration [s]', 'UTC']
TTFF_META_COL = ['Pwr On Time', 'Start Delay [s]', 'RF On Delay [s]' ]
CORR_META_COL = ['Pwr On Time', 'Start Delay [s]', 'RF On Delay [s]' ]
RFONOFF_META_COL = ['Corr Off Time [s]']
ALL_META_COL = COMM_META_COL + CONT_META_COL + REAQ_META_COL + TTFF_META_COL + RFONOFF_META_COL + CORR_META_COL
for each in [CONT_META_COL, REAQ_META_COL, TTFF_META_COL, RFONOFF_META_COL]:
  each += COMM_META_COL

NAV_METRIC_prefix = "GTTNAV"
NAV_scen = "continuousnav-roof"

TTFF_METRIC_prefix = "TTFFTest"
TTFF_scen = "ttff-roof"

REAQ_METRIC_prefix = "REAQTest"
REAQ_scen = "reacquisition-roof"

RFONOFF_METRIC_prefix = "RFONOFFTest"
RFONOFF_scen = "rf-on-off-roof"

CORR_METRIC_prefix = "CORRONOFFTest"
CORR_scen = "corr-on-off-roof"

# Histogram bucket stuff (TODO)
BOTTOM, TOP = (-3, 6)
RANGE = np.logspace(BOTTOM, TOP, TOP - BOTTOM + 1, endpoint=True)
# Insert 0.0 at the start of RANGE in order to account for values
# between 0.0 and 1.0e-3.
RANGE_WITH_0 = np.insert(RANGE, 0, 0.0 )
PERCENTILES = [0.01, 0.05, 0.25, 0.5, 0.68, 0.95, 0.99]                                                       
_mk_metric_id = lambda k: ('d%.3f' % k).replace('.', '_')

def get_args():
  parser = argparse.ArgumentParser(description="Swift Navigation GTT upload and csv plotting tool.")
  parser.add_argument("file",
                      help="the csv file to plot.")
  parser.add_argument('-o', '--outdir',
                      default='',
                      help='Store output artifacts in this directory.',)
  parser.add_argument('-p', '--plot',
                      help='Create plots.',
                      action="store_true") 
  parser.add_argument('-i', '--interactive',
                      help='Make plot windows interactive.',
                      action="store_true") 
  parser.add_argument('-s', '--serial_override',
                     help='Serial Number override (this will only be needed prior to the serial number having been implemented in settings).',
                      )
  parser.add_argument('-a', '--annotation',
                     help='string to add to every plot.',
                      )
  parser.add_argument('-m', '--metrics',
                      help='Create metrics.',
                      action="store_true") 
  parser.add_argument('-c', '--col',
                      default='',
                      help=('Substring of column title to plot. If blank, all columns that are not automatically'
                            'excluded will be plotted.  Has no effect for metrics.'),
                      )
  parser.add_argument('-n', '--navigation',
                      action='store_true',
                      help=('Generate GTTNAV metrics for each navigation cycle.'),
                      )
  parser.add_argument('-u', '--upload',
                      action="store_true", 
                      help=('Send to database?'),
                      )
  return parser.parse_args()

def rem_illegal_chars_column_name(input_column_name):
  return input_column_name.strip().replace(' ', '_').replace('/','p')

def rem_units_column_name(input_column_name):
  return re.sub("\s[\(\[].*?[\)\]]", "", input_column_name)

def filepath_column_name(input_column_name):
  return rem_illegal_chars_column_name(rem_units_column_name(input_column_name))

def flatten(d, parent_key='', sep=' '):
  items = []
  for k, v in d.items():
    new_key = rem_illegal_chars_column_name(parent_key) + sep + k if parent_key else k
    if isinstance(v, collections.MutableMapping):
      items.extend(flatten(v, new_key, sep=sep).items())
    else:
      items.append((new_key, v))
  return dict(items)

def plot_column_from_df(df, column_title, row_title, annotation=''):
  try: 
    fig = plt.figure(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
    ax1 = plt.subplot(3, 1, 1)
    ordinate = df[row_title]
    if ordinate.dtype == object:
      df.plot(x=row_title, y=column_title, ax=ax1, marker='x')
    else:
      plt.plot(ordinate, df[column_title], 'x')
    plt.title('{0}: {1}'.format(annotation, column_title))
    plt.ylabel(column_title)
    plt.xlabel(row_title)
    # Velocity histogram
    ax2 = plt.subplot(3, 1, 2)
    df[column_title].hist(ax=ax2)
    plt.xlabel("{0}".format(column_title))
    plt.ylabel("Number")
    plt.subplot(3,1,3)
    plt.figtext(0.25,0.1, "Statistics\n " + str(df[column_title].describe(percentiles=PERCENTILES)))
    if (df[column_title] > 0).any():
      return fig 
    else:
      return None 
  except:
    print "Error plotting column {0} against row {1}".format(column_title, row_title)
    import traceback
    print traceback.format_exc()

def read_in_file(datafile):
  return pd.read_csv(datafile)

def read_or_blank(path):
  if os.path.exists(path):
    with open(path, 'r') as f:
      return f.read()
  else:
    return ""

def parse_report(report):
  return_dict = {}
  lines = report.split('\n')
  for line in lines:
    keyvalue_list = line.split(':')
    if len(keyvalue_list) == 2:
      return_dict[keyvalue_list[0].strip()] = keyvalue_list[1].strip()
  print return_dict
  return return_dict

def system_info_dict():
  return {'sys_info': platform.uname(),
          'hostname': platform.node(),
          'hosttime': str(datetime.datetime.now())}
 
def main():
  """Simple command line interface for plotting up GTT nav.csvs"

  """
  fig_array = []
  title_array = []
  args = get_args()
  isnavtest = False
  # get all of our files ducks in a row
  df = read_in_file(args.file)
  # if a report.txt exists in csv dir, read it in to use for the "msg"
  # if an error.txt exists in csv dir, read it in to use for the "failures"
  dirname, filename = os.path.split(args.file)
  if args.outdir:
    outdir = args.outdir
  else:
    outdir = dirname
  report = read_or_blank((os.path.join(dirname, 'report.txt')))
  report_dict = parse_report(report)
  if report_dict:
    assert 'Firmware Version' in report_dict.keys()
    assert 'Serial Number' in report_dict.keys()
  if args.serial_override:
    serial = args.serial_override
  else:
    serial = 'PK' + report_dict['Serial Number']
  errors = read_or_blank((os.path.join(dirname, 'errors.txt'))) 
  # check what the filename is to determine the exclude list
  # if it doesn't match, try all known exclusion columns
  if filename == 'nav.csv':
    scen = NAV_scen
    navdf = df
    df = pd.DataFrame()
    metadata_columns = CONT_META_COL
    isnavtest = True
  elif filename == 'reacq-results.csv':
    scen = REAQ_scen
    prefix = REAQ_METRIC_prefix
    navdf = read_in_file(os.path.join(dirname, 'nav.csv'))
    ordinate = 'Start UTC'
    metadata_columns = REAQ_META_COL
  elif filename == 'starts.csv':
    scen =  TTFF_scen
    prefix = TTFF_METRIC_prefix
    navdf = read_in_file(os.path.join(dirname, 'nav.csv'))
    ordinate = 'Start UTC'
    metadata_columns = TTFF_META_COL
  elif filename == 'rf-on-off.csv':
    scen =  RFONOFF_scen 
    prefix = RFONOFF_METRIC_prefix
    navdf = read_in_file(os.path.join(dirname, 'nav.csv'))
    ordinate = 'Start UTC'
    metadata_columns = RFONOFF_META_COL
  elif filename == 'corr-on-off.csv':
    scen =  CORR_scen 
    prefix = CORR_METRIC_prefix
    navdf = read_in_file(os.path.join(dirname, 'nav.csv'))
    ordinate = 'Start UTC'
    metadata_columns = CORR_META_COL
  else:
    print "Unknown csv file, generictest used"
    scen = "GenericManual"
    prefix = "GenericGttTest"
    ordinate = 'TOW [s]'
    navdf = read_in_file(os.path.join(dirname, 'nav.csv'))
  
  # setup column filters based upon filename. Ignore null columns 
  c_exclude_filt = lambda col: col not in ALL_META_COL 
  if args.col:
    c_include_filt = lambda col: str(col).find(args.col) != -1
  else:
    c_include_filt = lambda col: True 
  print c_include_filt('Baseline')
  cols = [] 
  cols = [col for col in df.columns if c_exclude_filt(col) and c_include_filt(col) \
                                                           and df[col].notnull().any()] 
  navcols = [col for col in navdf.columns if c_exclude_filt(col) and c_include_filt(col) \
                                                            and navdf[col].notnull().any()]   
  if cols:
    print "Processing the following columns: {0}".format(cols)  
  if navcols:
    print "Processing the following Navigation columns: {0}".format(navcols)  
  

  # plot and build arrays of matplotlib figures / title strings for filenames 
  if args.plot:
    fig_array = [plot_column_from_df(df, col, ordinate, args.annotation) for col in cols]
    title_array = [filepath_column_name(col) for col in cols]
    fig_array += [plot_column_from_df(navdf, navcol, 'TOW [s]', args.annotation) for navcol in navcols]
    title_array += [filepath_column_name(navcol) for navcol in navcols]

    if args.interactive:
      plt.show()
    else:
      # Figures go in the "figures" subdirectory of the output directory
      if not os.path.exists(outdir):
        os.makedirs(outdir)
      figbase = os.path.join(outdir, 'figures')
      if not os.path.exists(figbase):
        os.makedirs(figbase)
      for fig, title in zip(fig_array, title_array):
        if fig:
          fig.savefig(os.path.join(figbase, title 
                      + '_' + os.path.split(os.path.split(args.file)[0])[1] + '.png'))
  
  # make metrics output
  if args.metrics:
    import json
    # For 1.1 we just make 1 set of metrics per test
    toplevel_metrics_dict = {}
    # We add the navigation DF columns if this is a nav.csv or the user asked for it
    # Metrics list is going to be a big list of dictionaries that take the form 
    # {testname: {metrics: [{key, value}]}}
    # There is one for each NAV cycle
    if args.navigation or isnavtest:
      metrics_dict = {}
      failure_reason = ''
      desc = navdf[navcols].describe(percentiles=PERCENTILES).dropna()
      desc_dict = desc.to_dict()
      for err in ERR_COLUMNS:
        failure_reason += "\n".join([e for e in navdf.get(err, pd.Series()).dropna()])
      # if we are continous we add the whole test execution errors to the blob
      toplevel_metrics_dict[NAV_METRIC_prefix] = {'metrics': desc_dict}
      # If this nav cycle has a failure reason, we add it to the metrics_dict for the cycle
      if failure_reason:
        toplevel_metrics_dict[NAV_METRIC_prefix].update({'failure_reason': {'all': failure_reason}})
      # TODO: Put all solution errors and similar in histogram bins rather than the "describe" found here
      # metrics_dict.set('failure_reasons', {"all": errors})
    # Make metrics from the test specific metrics (if they exist). 
    # One test Dict per row/cycle  
    # Errors go in failure reason
    column_dict = {} 
    failure_reason = ''
    if not isnavtest:
      for col in cols:
        column_dict[col] = df[col].describe(percentiles=PERCENTILES).dropna().to_dict()
      toplevel_metrics_dict[prefix] = {'metrics': column_dict}
      for err in ERR_COLUMNS:
        failure_reason += "\n".join([e for e in navdf.get(err, pd.Series()).dropna()])
      if failure_reason and isinstance(failure_reason, str):
        toplevel_metrics_dict[prefix].update({'failure_reason': {'all': failure_reason}})
    for _, each in toplevel_metrics_dict.iteritems():
      each['report'] = report
      each['upload_info'] = str(system_info_dict())
      each['errors'] = errors
      each['piksi_serial_number'] =  serial
    out_dict = {'piksi_run': 
                 [
                  toplevel_metrics_dict
                 ]
                } 
    with open(os.path.join(outdir, 'metrics_output.json'), 'w') as f:
      json.dump(out_dict, f) 
  
    # Now put in database if the user asked to
  if args.upload:
    print "Publishing not a feature here..."
      
if __name__ == "__main__":
  main()

