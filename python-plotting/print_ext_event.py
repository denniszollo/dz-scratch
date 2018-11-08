#!/usr/bin/env python2.7
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
from sbp.client import Framer, Handler
from sbp.client.drivers.file_driver import FileDriver
from sbp.ext_events import *

class EventExtractor(object):

    def _event_callback(self, msg):
        print "time of week is {0}".format(float(msg.tow) + msg.ns_residual/1e6)


def get_args():
    import argparse
    parser = argparse.ArgumentParser(description="write mag data to fil")
    parser.add_argument("file",
                        help="specify the SBP JSON file for which to dump observations to CSV.")
    parser.add_argument("-f", "--format", default="bin",
                        help="Input file format")
    return parser.parse_args()


def main():
    # open a file, iterate through it, 
    # do something when particular message type is found
    args = get_args()
    with open(args.file, 'r') as fd:
        if args.format == 'json':
            iterator=JSONLogIterator(fd).next()
        elif args.format == 'bin':
            driver = FileDriver(fd)
            iterator = Framer(driver.read, driver.write)
        else:
            raise("unknown format: possible formats are bin and json")
        conv = EventExtractor()
        while True:
          try:
            (msg, data) = iterator.next()
            if isinstance(msg, MsgExtEvent):
                conv._event_callback(msg)
          except StopIteration:
              break

if __name__ == "__main__":
    main()
