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
        msg = "can't parse verbosity specification of type '{}'"
        raise TypeError(msg.format(type(verbosity)))

    for element in verbosity_list:
        is_int = type(element) is int
        is_numeric_str = (isinstance(element, str) and
                          re.match("^[0-9]+$", element))
        if is_int or is_numeric_str:
            state['verbosity'] = int(element)
            msg = "set global console verbosity level {}"
            state['log'](0, "green").print(msg.format(state['verbosity']))
        elif isinstance(element, str):
            m = re.match("^(.+)=([0-9]+)$", element)
            if not m:
                msg = "can't parse verbosity specification '{}'"
                raise ValueError(msg.format(element))
            logger = get_logger(m.group(1))
            level = int(m.group(2))
            logger.verbosity(level)
            msg = "set console verbosity level {}={}"
            logger(0, "green").print(msg.format(m.group(1), level))


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
        msg = "can't parse verbosity specification of type '{}'"
        raise TypeError(msg.format(type(verbosity)))

    for element in verbosity_list:
        is_int = type(element) is int
        is_numeric_str = (isinstance(element, str) and
                          re.match("^[0-9]+$", element))
        if is_int or is_numeric_str:
            state['log_verbosity'] = int(element)
            if state['log_verbosity'] is not None:
                level = state['log_verbosity']
                msg = "set global log verbosity level {}"
                state['log'](0, "green").print(msg.format(level))
        elif isinstance(element, str):
            m = re.match("^(.+)=([0-9]+)$", element)
            if not m:
                msg = "can't parse verbosity specification '{}'"
                raise ValueError(msg.format(element))
            logger = get_logger(m.group(1))
            level = int(m.group(2))
            logger.log_verbosity(level)
            msg = "set log verbosity level {}={}"
            logger(0, "green").print(msg.format(m.group(1), level))
