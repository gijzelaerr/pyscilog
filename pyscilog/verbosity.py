import re
from typing import Union, List, Any
from pyscilog import get_logger
from pyscilog.state import State

state = State()


def set_verbosity(verbosity: Union[int, List[int], str, None]):
    if verbosity is None:
        state['verbosity'] = 0
        return
    # ensure verbosity is turned into a list.
    verbosity_list: List[Any]
    if type(verbosity) is int:
        verbosity_list = [verbosity]
    elif isinstance(verbosity, str):
        verbosity_list = verbosity.split(",")
    elif isinstance(verbosity, (list, tuple)):
        verbosity_list = list(verbosity)
    else:
        raise TypeError("can't parse verbosity specification of type '{}'".format(type(verbosity)))
    
    for element in verbosity_list:
        if type(element) is int or (isinstance(element, str) and re.match("^[0-9]+$", element)):
            state['verbosity'] = int(element)
            state['log'](0, "green").print("set global console verbosity level {}".format(state['verbosity']))
        elif isinstance(element, str):
            m = re.match("^(.+)=([0-9]+)$", element)
            if not m:
                raise ValueError("can't parse verbosity specification '{}'".format(element))
            logger = get_logger(m.group(1))
            level = int(m.group(2))
            logger.verbosity(level)
            logger(0, "green").print("set console verbosity level {}={}".format(m.group(1), level))


def get_verbosity(verbosity: Union[List[int], int, str, None]):
    if verbosity is None:
        state['log_verbosity'] = None  # None means follow console default
        return
    # ensure verbosity is turned into a list.
    verbosity_list: List[Any]
    if type(verbosity) is int:
        verbosity_list = [verbosity]
    elif isinstance(verbosity, str):
        verbosity_list = verbosity.split(",")
    elif isinstance(verbosity, (list, tuple)):
        verbosity_list = list(verbosity)
    else:
        raise TypeError("can't parse verbosity specification of type '{}'".format(type(verbosity)))
    
    for element in verbosity_list:
        if type(element) is int or (isinstance(element, str) and re.match("^[0-9]+$", element)):
            state['log_verbosity'] = int(element)
            if state['log_verbosity'] is not None:
                state['log'](0, "green").print("set global log verbosity level {}".format(state['log_verbosity']))
        elif isinstance(element, str):
            m = re.match("^(.+)=([0-9]+)$", element)
            if not m:
                raise ValueError("can't parse verbosity specification '{}'".format(element))
            logger = get_logger(m.group(1))
            level = int(m.group(2))
            logger.log_verbosity(level)
            logger(0, "green").print("set log verbosity level {}={}".format(m.group(1), level))
