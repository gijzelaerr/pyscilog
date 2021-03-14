from __future__ import print_function
import logging
import logging.handlers

from pyscilog.color import cprint
from pyscilog.filter import LogFilter, get_subprocess_label, set_subprocess_label
from pyscilog.handlers import _sigusr1_handler, _sigusr2_handler
from pyscilog.wrapper import LoggerWrapper, datefmt, set_boring, log_to_file
from pyscilog.state import State
from pyscilog.handlers import init_handlers

state = State()
init_handlers()


def get_log_filename():
    """
    Returns log filename if log_to_file has been called previously, None otherwise
    """
    if not state['file_handler']:
        return None
    return state['file_handler'].baseFilename


def enable_memory_logging(level=1):
    LogFilter.setMemoryLogging((level or 0) % 3)  # level is 0/1/2


def init(app_name):
    if state['root_logger'] is None:
        logging.basicConfig(datefmt=datefmt)
        state['app_name'] = app_name
        state['root_logger'] = logging.getLogger(app_name)
        state['root_logger'].setLevel(logging.DEBUG)
        state['log'] = state['loggers'][''] = LoggerWrapper(state['root_logger'])


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


def set_loud(log_name):
    """Un-silences the specified sublogger(s)"""
    state['log'].print(cprint("set loud: %s" % log_name, col="green"))
    if isinstance(log_name, str):
        get_logger(log_name).logger.setLevel(logging.DEBUG)
    elif type(log_name) is list:
        for name in log_name:
            get_logger(name).logger.setLevel(logging.DEBUG)
