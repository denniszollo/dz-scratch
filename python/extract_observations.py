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
from sbp.client.loggers.json_logger import JSONLogIterator
from sbp.observation import *

columns = [ "wn",
            "tow (ms)",
            "Constellation",
            "Identifier",
            "Pseudorange(m)",
            "Carrier Phase (cycles)"
            "CnO (db-hz)"
            "Lock_indicator (changes each carrier phase slip)"]


class ObsExtractor(object):
  def __init__(self, outfile):
    self.locks = {} # SID indexed dictionary with the last lock time
    self.last_header_tow = 0
    self.last_counter = 0
    self.outfile = outfile
    self.outfile.write(",".join(columns) + "\n")

  def obs_callback(self, msg):
    if(msg.sender == 0):
      return
    num_obs = msg.header.n_obs >> 4
    counter = msg.header.n_obs & ((1 << 4) - 1)
    # if the counter is 0, we reset everything
    if counter == 0:
      self.obs = msg.obs
      self.header = msg.header
      output = True
    # if the time of week is the same from the last header and we didn't skip a packet, update our obs
    #    previous header tow   current tow           previous counter + 1            current counter
    elif self.header.t.tow == msg.header.t.tow and (self.header.n_obs & 0x0F) + 1 == counter:
      for each in msg.obs:
        self.obs.append(each)
      self.header = msg.header
      output = True
    else:
      print "Dropped a packet, skipping the sequence."
      output = False
    if output and (counter+1) == num_obs:
      # do something with the complete set of observations
      for each in self.obs:
        if each.sid.code == 0:
          code = "GPSL1"
        elif each.sid.code == 1:
          code = "GPSL2"
        else:
          code = "unknown"
        self.outfile.write(("{0},{1},{2},{3},"
          "{4},{5},{6},{7}\n").format(self.header.t.wn,
          self.header.t.tow,
          code, each.sid.sat,
          float(each.P)/50.0,
          float(each.L.i) + float(each.L.f) / (1<<8),
          float(each.cn0) / 4.0,
          each.lock))

def get_args():
  import argparse
  parser = argparse.ArgumentParser(description="SBPJson to RTCM converter")
  parser.add_argument("file",
                      help="specify the SBP JSON file for which to dump observations to CSV.")
  parser.add_argument("-o", "--outfile", default="out.csv",
                      help="Output .csv file")
  return parser.parse_args()


def main():
  # First, we start up an SBP driver reading from STDInput
  first = True
  args = get_args()
  with open(args.file, 'r') as fd:
    with JSONLogIterator(fd) as log:
      with open(args.outfile, 'w+') as outfile:
        conv = ObsExtractor(outfile)
        mylog = log.next()
        while True:
          try:
            (msg, data) = mylog.next()
            if first:
              first = False
            print type(msg)
            if isinstance(msg, MsgObs):
              conv.obs_callback(msg)
          except StopIteration:
            break

if __name__ == "__main__":
  main()
