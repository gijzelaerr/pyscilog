import re
from typing import Union, List
from pyscilog import get_logger
from pyscilog.state import State

state = State()


def set_verbosity(verbosity: Union[int, List[int], str]):
    if verbosity is None:
        state['verbosity'] = 0
        return
    # ensure verbosity is turned into a list.
    if type(verbosity) is int:
        verbosity = [verbosity]
    elif isinstance(verbosity, str):
        verbosity = verbosity.split(",")
    elif not isinstance(verbosity, (list, tuple)):
        raise TypeError("can't parse verbosity specification of type '{}'".format(type(verbosity)))
    for element in verbosity:
        if type(element) is int or re.match("^[0-9]+$", element):
            state['verbosity'] = int(element)
            state['log'](0, "green").print("set global console verbosity level {}".format(state['verbosity']))
        else:
            m = re.match("^(.+)=([0-9]+)$", element)
            if not m:
                raise ValueError("can't parse verbosity specification '{}'".format(element))
            logger = get_logger(m.group(1))
            level = int(m.group(2))
            logger.verbosity(level)
            logger(0, "green").print("set console verbosity level {}={}".format(m.group(1), level))


def get_verbosity(verbosity: Union[List[int], int, str]):
    if verbosity is None:
        state['log_verbosity'] = None  # None means follow console default
        return
    # ensure verbosity is turned into a list.
    if type(verbosity) is int:
        verbosity = [verbosity]
    elif isinstance(verbosity, str):
        verbosity = verbosity.split(",")
    elif not isinstance(verbosity, (list, tuple)):
        raise TypeError("can't parse verbosity specification of type '{}'".format(type(verbosity)))
    for element in verbosity:
        if type(element) is int or re.match("^[0-9]+$", element):
            state['log_verbosity'] = int(element)
            if state['log_verbosity'] is not None:
                state['log'](0, "green").print("set global log verbosity level {}".format(state['log_verbosity']))
        else:
            m = re.match("^(.+)=([0-9]+)$", element)
            if not m:
                raise ValueError("can't parse verbosity specification '{}'".format(element))
            logger = get_logger(m.group(1))
            level = int(m.group(2))
            logger.log_verbosity(level)
            logger(0, "green").print("set log verbosity level {}={}".format(m.group(1), level))
