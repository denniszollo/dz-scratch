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
from sbp.imu import *

columns = [ "tow (ms)",
            "acc_x",
            "acc_y",
            "acc_z",
            "mag"]


class MagExtractor(object):
  def __init__(self, outfile):
    self.outfile = outfile
    self.outfile.write(",".join(columns) + "\n")

  def mag_callback(self, msg):
        self.outfile.write("{0},{1},{2},{3},{4}\n".format(msg.tow,
                           msg.acc_x, msg.acc_y, msg.acc_z, 
                           math.sqrt(msg.acc_x**2 + msg.acc_y**2 + msg.acc_z**2)))

def get_args():
  import argparse
  parser = argparse.ArgumentParser(description="write mag data to fil")
  parser.add_argument("file",
                      help="specify the SBP JSON file for which to dump observations to CSV.")
  parser.add_argument("-o", "--outfile", default="",
                      help="Output .csv file prefix")
  parser.add_argument("-f", "--format", default="binary",
                      help="Output .csv file")
  return parser.parse_args()


def main():
  # First, we start up an SBP driver reading from STDInput
  first = True
  args = get_args()
  outfile_str = ""
  with open(args.file, 'r') as fd:
    if args.format == 'json':
        iterator=JSONLogIterator(fd)
    elif args.format == 'bin':
        driver = FileDriver(fd)
        iterator = Framer(driver.read, driver.write)
    else:
        raise("unkonwn format")
    outfile_str = args.outfile + args.file + "imu.csv"
    with open(outfile_str, 'w') as outfile:
      conv = MagExtractor(outfile)
      if args.format == 'json':
         iterator = iterator.next()
      while True:
        try:
          (msg, data) = iterator.next()
          if first:
            first = False
          if isinstance(msg, MsgImuRaw):
            conv.mag_callback(msg)
        except StopIteration:
          break 
          
  df = pd.read_csv(open(outfile_str, 'r'))
  fig = plt.figure(figsize=[20,10])
  fig = plt.figure(figsize=[20,10])
  plt.subplot(3,1,1)
  plt.plot(df["tow (ms)"], df["tow (ms)"].diff())
  plt.ylabel(['tow period (milliseconds)'])
  ax = plt.subplot(3,1,2)
  df["tow (ms)"].diff().hist(ax=ax)
  fig.savefig(args.file + '.png')

if __name__ == "__main__":
  main()
