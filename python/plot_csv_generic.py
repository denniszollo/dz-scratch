#!/usr/bin/env python
# Copyright (C) 2015 Swift Navigation Inc.
# Contact: Dennis Zollo <dzollo@swift-nav.com>
#
# This source is subject to the license found in the file 'LICENSE' which must
# be be distributed together with this source. All other rights reserved.
#
# THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
# EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.

import sys
import math
import pandas as pd
import matplotlib.pyplot as plt 

from sbp.client.loggers.json_logger import JSONLogIterator
from sbp.client import Framer, Handler
from sbp.client.drivers.file_driver import FileDriver
from sbp.navigation import *
from sbp.orientation import *
from sbp.observation import *
from sbp.vehicle import *
from sbp.imu import *

def get_list_of_columns(MsgClassName):
    msgclass = eval(MsgClassName)
    return msgclass.__slots__

class MsgExtractor(object):
  def __init__(self, outfile, msgclassname):
    self.outfile = outfile
    self.columns = get_list_of_columns(msgclassname)
    self.outfile.write(",".join(self.columns) + "\n")

  def _callback(self, msg):
      for each in self.columns:
          self.outfile.write("{0},".format(getattr(msg, each)))
      self.outfile.write("\n")
def get_args():
  import argparse
  parser = argparse.ArgumentParser(description="write mag data to fil")
  parser.add_argument("file",
                      help="specify the SBP JSON file for which to dump observations to CSV.")
  parser.add_argument("-o", "--outfile", default="out.csv",
                      help="Output .csv file postfix")
  parser.add_argument("-t", "--type", default="MsgBaselineNed",
                      help="Message Type to csvify")
  parser.add_argument("-f", "--format", default="binary",
                      help="Output .csv file")
  return parser.parse_args()


def main():
  # First, we start up an SBP driver reading from STDInput
  first = True
  args = get_args()
  with open(args.file, 'r') as fd:
    if args.format == 'json':
        iterator=JSONLogIterator(fd)
    elif args.format == 'bin':
        driver = FileDriver(fd)
        iterator = Framer(driver.read, driver.write)
    else:
        raise("unkonwn format")
    with open(args.type + "_" + args.outfile, 'w+') as outfile:
      conv = MsgExtractor(outfile, args.type)
      if args.format == 'json':
         iterator = iterator.next()
      while True:
        try:
          (msg, data) = iterator.next()
          if first:
            first = False
          if isinstance(msg, eval(args.type)):
            conv._callback(msg)
        except StopIteration:
          break 
          
#  df = pd.read_csv(open(args.outfile, 'r'))
#  fig = plt.figure(figsize=[20,10])
#  plt.plot(df["tow (ms)"], df['acc_x'])
#  plt.legend(['acc_x'])
#  fig.savefig('acc.png')

if __name__ == "__main__":
  main()
