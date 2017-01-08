#!/usr/bin/python3.5

import yaml
import os.path
import logging

logger = logging.getLogger('hive')

config = None

# load the configuration file in
def load_config(filepath):
    global config
    with open(filepath, "r") as file_descriptor:
        config = yaml.load(file_descriptor)
    logger.debug("Config: ", config)

# Returns a list of tuplets (of commands src and destination)
def get_ips():
    ips = config['hive']['presence']['ips']
    return ips

def get_log_path():
    if config == None: exit("You must load the config first")
    return config['hive']['log']

def get_presence_transition_limit():
    if config == None: exit("You must load the config first")
    return config['hive']['presence']['limit']

def get_presence_period():
    if config == None: exit("You must load the config first")
    return config['hive']['presence']['period']

def get_hive_username():
    if config == None: exit("You must load the config first")
    return config['hive']['account']['username']

def get_hive_password():
    if config == None: exit("You must load the config first")
    return config['hive']['account']['password']

