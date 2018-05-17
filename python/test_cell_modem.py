import sys
import os
import time
import threading
from collections import OrderedDict

from sbp.client import Forwarder, Framer, Handler
from sbp.table import dispatch
from piksi_tools.settings import Settings
import piksi_tools.serial_link as sl
from sbp.logging import MsgLog, SBP_MSG_LOG
from sbp.piksi import SBP_MSG_RESET, MsgReset
from sbp.settings import (SBP_MSG_SETTINGS_WRITE, MsgSettingsWrite,
                          SBP_MSG_SETTINGS_WRITE_RESP, MsgSettingsWriteResp)


class LoopTimer(object):
    """
    The :class:`LoopTimer` calls a function at a regular interval.
    It is intended to be instantiated from a subclass instance of TestState to call
    TestStateSubclass.action() at a regular interval. The implementation is emulated
    from a simliar instance submitted via stack overflow
    http://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds

    Parameters
    ----------
    interval: int
      number of seconds between calls
    hfunction : handle to function
      function to call periodically
    """
    def __init__(self, interval, hfunction):
        self.interval = interval
        self.hfunction = hfunction
        self.thread = threading.Timer(self.interval, self.handle_function)

    def handle_function(self):
        """
        Handle function is called each time the timer trips.
        It sets up another timer to call itself again in the future.
        """
        self.hfunction()
        self.thread = threading.Timer(self.interval, self.handle_function)
        self.start()

    def start(self):
        """
        Starts the periodic timer thread.
        """
        print "in start"
        self.thread.start()

    def cancel(self):
        """
        Cancels any current timer threads.
        """
        if self.thread != None:
            self.thread.cancel()
            self.thread = None

    def reset(self):
        """
        Resets the periodic timer thread.
        """
        print "in reset"
        self.cancel()
        self.thread = threading.Timer(self.interval, self.handle_function)
        self.start()

class TestState(object):
    """
    Super class for representing state and state-based actions during logging.

    Parameters
    ----------
    handler: sbp.client.handler.Handler
        handler for SBP transfer to/from Piksi.
    filename : string
      File to log to.
    """
    def __init__(self, handler, interval):
        self.init_time = time.time()
        self.handler = handler
        self.timer = LoopTimer(interval, self.action)
        handler.add_callback(self.process_message)

    def __enter__(self):
        self.timer.start()
        return self

    def __exit__(self, *args):
        self.timer.cancel()

    def process_message(self, msg, **kwargs):
        """
        Stub for processing messages from device. Should be overloaded in sublcass.
        """
        raise NotImplementedError("action not implemented!")

    def action(self):
        """
        Stub for communicating with device. Should be overloaded in subclass.
        """
        raise NotImplementedError("action not implemented!")

class CellModemTestState(TestState):
    """
    Cell modem testing class representing state and state-based actions while cell modem
    is discovered.

    Parameters
    ----------
    handler: sbp.client.handler.Handler
        handler for SBP transfer to/from Piksi.
    interval : period after which to call "action" function
        File to log to.
    filename : string
        File to log to.
    commanded_cycles: int
        number of actions to do, if None, go forever
    """
    def __init__(self, handler, interval, filename='out.csv', commanded_cycles=None):
        super(CellModemTestState, self).__init__(handler, interval)
        self.state = 'PRE_INIT'
        self.state_tuples = [
         ('PRE_INIT'      , 'initialization of class / invalid'),
         ('INIT'          , 'Starting Up'),
         ('MFG'           , 'Received Modem Manufacturer'),
         ('MODEL'         , 'Received Modem Model'),
         ('REV'           , 'Received Modem Revision'),
         ('SN'            , 'Received Modem Serial Number'),
         ('SETTINGS_START', 'Cell Modem Settings Write Attempt'),
         ('SETTINGS_DONE' , 'Cell Modem Settings Write Success'),
         ('AT_START'      , 'One AT command resp'),
         ('AT_SUCCESS'    , 'Cell Modem HDW success'),
         ('CONNECT_FAIL'  , 'Cell Modem connect fail'),
         ('NAP_FAIL'      , 'Nap verification failed'),
         ('SETTINGS_FAIL' , 'Unable to write Settings'),
         ('TIMEOUT'       , 'Timeout')]
        self.state_desc = dict(self.state_tuples)
        keys = [shortname for shortname, _ in self.state_tuples]
        self.state_num_dict = dict(zip(keys, range(0, len(keys))))
        self.filename = filename
        with open(self.filename, 'w') as file:
            file.write(','.join([str(self.state_desc[key]) for key, _ in self.state_tuples]) + '\n')
        self.reset_time = 0
        self.state_dict = {}
        self.commanded_cycles = commanded_cycles
        self.handler = handler
        self.num_cycles = 0

    def log_state_trans(self, state):
        self.state_desc[state] # check that state is there for programmer
        self.state_dict[state] = time.time() - self.reset_time
        self.state = state
        print "State transition to state {0}, after {1} seconds". format(self.state, self.state_dict[self.state])

    def clear_state(self):
        self.state = 'INIT'
        for key in self.state_desc.keys():
            self.state_dict[key] = 0

    def log_state_dict(self):
        self.file = open(self.filename, 'a')
        self.file.write(','.join([str(self.state_dict[key]) for key, _ in self.state_tuples])+ '\n')

    def __enter__(self, *args):
        self.timer.start()
        self.reboot_and_log()
        self.reset_time = time.time()
        return self

    def __exit__(self, *args):
        self.timer.cancel()
        self.file.close()

    def state_within(self, lower, upper):
        upper_num = self.state_num_dict[upper]
        lower_num = self.state_num_dict[lower]
        current = self.state_num_dict[self.state]
        return current >= lower_num and current <= upper_num

    def do_settings(self):
        with Settings(self.handler) as settings:
            try:
                settings.write("cell_modem", "debug", "True", verbose=True,
                        write_retries=20, confirm_retries=20)
                if settings.read("cell_modem", "enable", retries=20, verbose=True):
                    print("Cell modem already enabled; toggling setting.")
                    settings.write("cell_modem", "enable", "False", verbose=True,
                        write_retries=20, confirm_retries=20)
                    time.sleep(10)
                settings.write("cell_modem", "enable", "True", verbose=True,
                    write_retries=20, confirm_retries=20)
            except RuntimeError as e:
                print(e)
                self.log_state_trans(9)
                self.handler.stop()
                sys.exit(-1)
                self.reboot_and_log()
                # settings write successful
            self.settings_done = True
            self.log_state_trans('SETTINGS_DONE')

    def process_message(self, msg, **kwargs):
        """
        Wait for logs and go through states.
        """
        msg = dispatch(msg)
        if  self.state == 0:
            self.state = 1    
        if isinstance(msg, MsgLog):
            print(msg.text)
            if self.state_within('INIT', 'SN'):
                if msg.text.startswith("piksi_system_daemon:"):
                    if msg.text.find("Modem Manufacturer: Telit") != -1:
                        self.log_state_trans('MFG')
                    elif msg.text.find("Modem Model:") != -1:
                        self.log_state_trans('MODEL')
                    elif msg.text.find("Modem Revision") != -1:
                        self.log_state_trans('REV')
                    elif msg.text.find("Modem Serial Number") != -1:
                        self.log_state_trans('SN')
            if self.state == 'SN':
                threading.Thread(target=self.do_settings).start()
                self.log_state_trans('SETTINGS_START')
            if self.state_within('SETTINGS_START', 'SETTINGS_DONE'):
                if msg.text.find("OK") != -1:
                    self.log_state_trans('AT_ATTEMPT')
            if self.state == 'AT_ATTEMPT':
                if msg.text.find("AT+COPS?") != -1:
                    self.log_state_trans('AT_SUCCESS')
                    self.reboot_and_log()
            if self.state_within('SN', 'NAP_FAIL') and self.state != 'CONNECT_FAIL':
                if msg.text == "Connect script failed":
                    self.log_state_trans('CONNECT_FAIL')
            if msg.text.startswith("NAP Verification"):
                print("Received Nap Verification Error.")
                self.log_state_trans('NAP_FAIL')
                self.reboot_and_log()
          
    def reboot_and_log(self):
        if self.state_dict:
            self.log_state_dict()
        self.num_cycles += 1
        if self.commanded_cycles != None and self.num_cycles > self.commanded_cycles:
            print("Completed {} commanded cycles.".format(self.commanded_cycles))
            self.timer.cancel()
            self.file.close()
            self.handler.stop()
            sys.exit(0)
        else:
            print("Starting {} cycles of {} cycles".format(self.num_cycles, self.commanded_cycles))
            self.clear_state()
            self.reset_time = time.time()
            self.timer.reset()
            self.handler(MsgReset(flags=0))
            time.sleep(0.25)

    def action(self):
        """
        Stub for communicating with device. Should be overloaded in subclass.
        """
        print "Hit interval timer after {0} seconds".format(time.time() - self.reset_time)
        self.log_state_trans('TIMEOUT')
        self.reboot_and_log()

def get_args():
    """
    Get and parse arguments.
    """
    import argparse
    parser = sl.base_cl_options()
    parser.add_argument("-i", "--interval",
                        default=[120], nargs=1,
                        help="Number of seconds between test attempts.")
    parser.add_argument("--timeout",
                        default=None,
                        help="Maximum time for test (even if cycles are not reached)")
    parser.add_argument("--outfile",
                        default="CellModemTestState.csv",
                        help="output csv file.")
    parser.add_argument("--cycles",
                        default=None,
                        help="number of cycles to try.")
    return parser.parse_args()



def main():
    """
    Get configuration, get driver, get logger, and build handler and start it.
    Create relevant TestState object and perform associated actions.
    Modeled after serial_link main function.
    """
    args = get_args()
    port = args.port
    baud = args.baud
    timeout = args.timeout
    log_filename = args.logfilename
    log_dirname = args.log_dirname
    if not log_filename:
        log_filename = sl.logfilename()
    if log_dirname:
        log_filename = os.path.join(log_dirname, log_filename)
    interval = int(args.interval[0])
    # Driver with context
    with sl.get_driver(args.ftdi, port, baud) as driver:
        # Handler with context
        with Handler(Framer(driver.read, driver.write, args.verbose)) as link:
            # Logger with context
            with sl.get_logger(args.log, log_filename, expand_json=args.expand_json) as logger:
                Forwarder(link, logger).start()
                try:
                    # Get device info
                    # add Teststates and associated callbacks
                    with CellModemTestState(link, interval, filename=args.outfile,
                                            commanded_cycles=int(args.cycles)) as cell:
                        cell.timer.thread.join()

                        if timeout is not None:
                            expire = time.time() + float(args.timeout)

                        while True:
                            if timeout is None or time.time() < expire:
                            # Wait forever until the user presses Ctrl-C
                                time.sleep(1)
                            else:
                                print "Timer expired!"
                                break
                            if not link.is_alive():
                                sys.stderr.write("ERROR: Thread died!")
                                sys.exit(1)
                except KeyboardInterrupt:
                    # Callbacks call thread.interrupt_main(), which throw a KeyboardInterrupt
                    # exception. To get the proper error condition, return exit code
                    # of 1. Note that the finally block does get caught since exit
                    # itself throws a SystemExit exception.
                    sys.exit(1)

if __name__ == "__main__":
    main()
