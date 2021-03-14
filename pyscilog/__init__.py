from __future__ import print_function
import logging
import logging.handlers
import os
from io import TextIOWrapper
from typing import Optional

import signal

from pyscilog.color import cprint
from pyscilog.filter import LogFilter, get_subprocess_label, set_subprocess_label
from pyscilog.wrapper import LoggerWrapper, datefmt, set_boring, log_to_file
from pyscilog.state import State

state = State()
state['silent']: bool = False

# this will be the handler for the log file
state['file_handler']: Optional[TextIOWrapper] = None

# dict of logger wrappers created by the application
state['loggers'] = {}


def get_log_filename():
    """
    Returns log filename if log_to_file has been called previously, None otherwise
    """
    if not state['file_handler']:
        return None
    return state['file_handler'].baseFilename


def enableMemoryLogging(level=1):
    LogFilter.setMemoryLogging((level or 0) % 3)  # level is 0/1/2


def _sigusr1_handler(signum, frame):
    level = 2 if LogFilter._log_memory == 1 else 1
    print("pid {} received USR1: memory logging level {}".format(os.getpid(), level))
    LogFilter.setMemoryLogging(level)


def _sigusr2_handler(signum, frame):
    print("pid {} received USR2: disabling memory logging".format(os.getpid()))
    LogFilter.setMemoryLogging(0)


signal.signal(signal.SIGUSR1, _sigusr1_handler)
signal.signal(signal.SIGUSR2, _sigusr2_handler)

state['root_logger'] = None
state['log'] = None


def init(app_name):
    if state['root_logger'] is None:
        logging.basicConfig(datefmt=datefmt)
        state['app_name'] = app_name
        state['root_logger'] = logging.getLogger(app_name)
        state['root_logger'].setLevel(logging.DEBUG)
        state['log'] = state['loggers'][''] = LoggerWrapper(cprint)


def get_logger(name, verbose=None, log_verbose=None):
    """Creates a new logger (or returns one, if already created)"""
    init("app")
    if name in state['loggers']:
        return state['loggers'][name]

    logger = logging.getLogger("{}.{}".format(state['app_name'], name))
    lw = state['loggers'][name] = LoggerWrapper(logger, verbose, log_verbose)
    lw(2).print("logger initialized")

    return lw


def set_silent(log_name):
    """Silences the specified sublogger(s)"""
    state['log'].print(cprint("set silent: %s" % log_name, col="red"))
    if isinstance(log_name, str):
        get_logger(log_name).logger.setLevel(logging.CRITICAL)
    elif type(log_name) is list:
        for name in log_name:
            get_logger(name).logger.setLevel(logging.CRITICAL)


def set_load(log_name):
    """Un-silences the specified sublogger(s)"""
    state['log'].print(cprint("set loud: %s" % log_name, col="green"))
    if isinstance(log_name, str):
        get_logger(log_name).logger.setLevel(logging.DEBUG)
    elif type(log_name) is list:
        for name in log_name:
            get_logger(name).logger.setLevel(logging.DEBUG)
