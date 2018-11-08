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
from sbp.client.loggers.json_logger import JSONLogIterator
from sbp.orientation import *
from sbp.navigation import *
import pandas as pd
import matplotlib.pyplot as plt

columns = [ "tow (ms)",
            "roll",
            "pitch",
            "yaw",
            "yaw_deg",
            "cog_deg"]


class EulerExtractor(object):
  def __init__(self, outfile):
    self.outfile = outfile
    self.outfile.write(",".join(columns) + "\n")
    self.vn = 0
    self.ve = 0

  def _euler_callback(self, msg):
        self.outfile.write("{0},{1},{2},{3},{4},{5}\n".format(msg.tow,
                           msg.roll, msg.pitch, msg.yaw, msg.yaw/1000000, math.atan2(self.ve, self.vn)*180/math.pi))

  def _vel_callback(self, msg):
      self.vn = msg.n
      self.ve = msg.e

def get_args():
  import argparse
  parser = argparse.ArgumentParser(description="write mag data to fil")
  parser.add_argument("file",
                      help="specify the SBP JSON file for which to dump observations to CSV.")
  parser.add_argument("-o", "--outfile", default="out.csv",
                      help="Output .csv file")
  parser.add_argument("-p", "--plot-only", action="store_true",
                      help="skip_conversion")
  return parser.parse_args()


def main():
  # First, we start up an SBP driver reading from STDInput
  first = True
  args = get_args()
  if not args.plot_only:
    with open(args.file, 'r') as fd:
      with JSONLogIterator(fd) as log:
        with open(args.outfile, 'w+') as outfile:
          conv = EulerExtractor(outfile)
          mylog = log.next()
          while True:
            try:
              (msg, data) = mylog.next()
              if first:
                first = False
              if isinstance(msg, MsgOrientEuler):
                conv._euler_callback(msg)
              if isinstance(msg, MsgVelNED):
                conv._vel_callback(msg)
            except StopIteration:
              break
    conv.outfile.close()
  df = pd.read_csv(open(args.outfile, 'r'))
  fig = plt.figure(figsize=[20,10])
  plt.plot(df["tow (ms)"], df['yaw_deg']+53)
  plt.plot(df["tow (ms)"], df['cog_deg'])
  plt.legend(['yaw (plus 53 degrees)','cog'])
  fig.savefig('yaw.png')


    


if __name__ == "__main__":
  main()
