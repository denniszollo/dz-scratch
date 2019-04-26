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
from sbp.piksi import *

columns = [ "sequence",
            "response"]


class Extractor(object):
  def __init__(self, outfile):
    self.outfile = outfile
    self.outfile.write(",".join(columns) + "\n")
    self.last_status = None

  def _callback(self, msg):
      if self.last_status is not None:
          assert msg.code == self.last_status+1, "skipped a code {0} : {1}".format(msg.code, self.last_status)
      self.last_status = msg.code

def get_args():
  import argparse
  parser = argparse.ArgumentParser(description="write mag data to fil")
  parser.add_argument("file",
                      help="specify the SBP JSON file for which to dump observations to CSV.")
  parser.add_argument("-o", "--outfile", default="out.csv",
                      help="Output .csv file")
  parser.add_argument("-f", "--format", default="bin",
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
    with open(args.outfile, 'w+') as outfile:
      conv = Extractor(outfile)
      if args.format == 'json':
         iterator = iterator.next()
      while True:
        try:
          (msg, data) = iterator.next()
          if first:
            first = False
          if isinstance(msg, MsgCommandResp):
            conv._callback(msg)
        except StopIteration:
          break 
          
  df = pd.read_csv(open(args.outfile, 'r'))
  fig = plt.figure(figsize=[20,10])
  plt.plot(df["tow (ms)"], df['acc_x'])
  plt.legend(['acc_x'])
  fig.savefig('acc.png')

if __name__ == "__main__":
  main()
