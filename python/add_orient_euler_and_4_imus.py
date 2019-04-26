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

from sbp.client.loggers.json_logger import JSONLogIterator
from sbp.client import Framer
from sbp.client.drivers.file_driver import FileDriver
from sbp.table import _SBP_TABLE
from sbp.orientation import MsgOrientEuler, SBP_MSG_ORIENT_EULER
from sbp.imu import SBP_MSG_IMU_RAW
import construct
import math

class MsgExtractor(object):
    def __init__(self, outfile, msgclass, metadata=False):
        self.outfile = outfile
        self.columns = get_list_of_columns(msgclass, metadata)
        print("selected columns are: {}".format("\n    ".join(self.columns)))
        self.outfile.write(",".join(self.columns) + "\n")

    def _callback(self, msg, data):
        outstringlist = []
        for each in self.columns:
            try:
                attr = getattr(msg, each)
                if isinstance(attr, construct.lib.ListContainer):
                    for list_element in attr:
                        outstringlist.append("{0}".format(list_element))
                else:
                    outstringlist.append("{0}".format(attr))
            except AttributeError:
                outstringlist.append("{0}".format(data[each]))
        self.outfile.write(",".join(outstringlist) + "\n")


class MsgInjector(object):
    def __init__(self, outfile, msgclass, metadata=False):
        self.outfile = outfile
        self.counter = 0;
        self.sawtooth_indexer = 0;

    def any_callback(self, msg, data):
         self.outfile.write(msg.to_binary())

    def create_orient_euler(self, tow):
        msg_dict = {'msg_type': SBP_MSG_ORIENT_EULER,
                    'sender_id': 0,
                    'tow':tow,
                    'roll': 0,
                    'pitch': 0,
                    'yaw': 0,
                    'roll_accuracy': 0.1,
                    'pitch_accuracy': 0.1,
                    'yaw_accuracy': 180,
                    'flags': 1
                    }
        sawtooth_value = 45 * math.sin(self.counter/10000.0 * 2 * math.pi) * 1e6
        if self.sawtooth_indexer == 0:
            msg_dict['pitch'] = sawtooth_value
        else:
            msg_dict['roll'] = sawtooth_value
        self.counter += 1
        if self.counter % 10000 == 0:
            self.counter = 0;
            self.sawtooth_indexer += 1
            self.sawtooth_indexer &= 1
        msg = MsgOrientEuler(**msg_dict)
        return msg

    def send_group_with_sender_id(self, sender_id, imu_raw_msg, orient_template):
         imu_raw_msg.sender = sender_id
         orient_template.sender = sender_id
         imu_raw_msg.tow != 0x80000000 # remove high bit if set
         self.outfile.write(imu_raw_msg.to_binary())
         self.outfile.write(orient_template.to_binary())
    
    def imu_raw_callback(self, msg, data):
         orient_template = self.create_orient_euler(msg.tow)
         self.send_group_with_sender_id(100, msg, orient_template)
         self.send_group_with_sender_id(101, msg, orient_template)
         self.send_group_with_sender_id(102, msg, orient_template)
         self.send_group_with_sender_id(103, msg, orient_template)

def get_args():
    import argparse
    parser = argparse.ArgumentParser(
        description="write msg fields to a csv file, one column per field")
    parser.add_argument("file",
                        help="specify the SBP JSON/binary file for which to dump fields to CSV.")
    parser.add_argument("-o", "--outfile", default="out.csv",
                        help="Output .csv file postfix")
    parser.add_argument("-f", "--format", default="binary",
                        help="Input Format (bin or json)")
    return parser.parse_args()


def main():
    args = get_args()
    open_args = 'rb' if args.format == 'bin' else 'r'
    with open(args.file, open_args) as fd:
        if args.format == 'json':
            iterator = JSONLogIterator(fd)
        elif args.format == 'bin':
            driver = FileDriver(fd)
            iterator = Framer(driver.read, driver.write)
        else:
            raise Exception(
                "Usage Error: Unknown input format. Valid input formats for -f arg are bin and json.")
        msg_class = None
        with open(args.outfile, 'wb') as outfile:
            conv = MsgInjector(outfile, msg_class, metadata=(args.format == 'json'))
            if args.format == 'json':
                iterator = iterator.next()
            while True:
                try:
                    (msg, data) = iterator.next()
                    if msg.msg_type == SBP_MSG_IMU_RAW:
                        conv.imu_raw_callback(msg, data)
                    else:
                        conv.any_callback(msg, data)
                except StopIteration:
                    break

if __name__ == "__main__":
    main()
