#!/usr/bin/python3.5
 
from subprocess import run, CalledProcessError, PIPE
import sys, time
import argparse
import logging
import os
from utils.daemon import Daemon
from utils.hive import login, get_mode, set_mode
from utils.config import load_config, get_log_path, get_ips, get_presence_transition_limit, get_presence_period 
from utils.logger import setupLogger

class hiveControl(Daemon):
    def run(self):
        global args
        print ('Run')
        sys.stderr.write('Run')

        # Logging
        print('test')
        config_file = args.config #"/mnt/storage/users/kieronc/git/hive/etc/config.yml"
        load_config(config_file)
        log_path = get_log_path()
        setupLogger(log_path, args.verbose)
        logger = logging.getLogger('hive')
        login() 
        # Scenarios
        """
        1) XXX Heating is off and someone comes home => Mode: SCHEDULE
        2) XXX Heating is on and someone leave house, but someone is still home => Mode: No change
        3) XXX Heating is on and everyone leaves the house => Mode: OFF
        4) Heating is is turned on remotley and no-one is at home. => Mode: No change
        5) XXX Heating is set to BOOST => Mode: No change
        """

        # Initial variables
        state_counter = 0       #how long has the state differed for

        # Get the initial state
        current_state = get_mode()
        next_state = current_state

        # Read in the config
        state_transition_limit = get_presence_transition_limit()        
        period = get_presence_period()        

        # get the congig/IPs
        ips = get_ips()
           
        while True:

            next_state = 'OFF'
            # Loop through the IPs
            for ip in ips:
                    
                # Ping the IP
                ping_cmd = "ping -c1 " + ip
                try:
                    status = os.system(ping_cmd)
                except CalledProcessError as e:
                    logger.error ("STDout: %s", CalledProcessError.output)
               
                logger.debug("%s -> %s", ip, status)
                
                # If we get a response, then we are done, so exit the loop
                if status == 0:
                    next_state = 'HEAT'
                    break

            # If the state hasn't changed 
            logger.debug("next_state: %s", next_state)
            logger.debug("current_state: %s", current_state)
            if next_state == current_state:
                time.sleep(period)
                state_counter = 0       # Reset the state counter as someone is at home
                continue

            # 5) If we are in boost mode do nothing
            if current_state == 'BOOST':
                logger.debug("Boost state, sleeping for 10 minutes")
                time.sleep(600)
                current_state = get_mode()
                state_counter = 0       # Reset the state counter as someone is at home
                continue

            # Increment the counter
            state_counter+=1

            # States differ, but haven't been different for long enough
            if state_counter < state_transition_limit:
                logger.debug("state_counter -> state_transition_limit: %s -> %s", state_counter, state_transition_limit)
                # If we are turning the heat off, wait for the delays. If turning the heat on then don't wait. 
                if current_state == 'HEAT' and next_state == 'OFF':
                    time.sleep(period)
                continue

            # Update the current state
            current_state = get_mode()

            # 3) Turn the heating off
            if current_state == 'HEAT' and next_state == 'OFF':
                # If delay_counter is greater than delay config, then issue command to hive
                set_mode('OFF')
                current_state = 'OFF'
            # 1) Turn the heating on
            elif current_state == 'OFF' and next_state == 'HEAT':
                set_mode('HEAT')
                current_state = 'HEAT'

            # Reset the counter
            state_counter = 0

if __name__ == "__main__":
    daemon = hiveControl('/tmp/hive.pid')
    #global args 
    # Parse the input params
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="start|stop|restart", type=str)
    parser.add_argument("--verbose", help="Run in debug mode", action="store_true")
    parser.add_argument("--config", help="Config file", type=str, default="/etc/config.yml")
    args = parser.parse_args()

    if 'start' == args.action:
        daemon.start()
    elif 'stop' == args.action:
        daemon.stop()
    elif 'restart' == args.action:
        daemon.restart()
    else:
        print ("Unknown command")
        sys.exit(2)
    sys.exit(0)
