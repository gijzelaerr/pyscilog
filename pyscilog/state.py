import os
import psutil


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class State(dict):
    pass


state = State()
state['silent'] = False

# this will be the handler for the log file
state['_file_handler'] = None

# dict of logger wrappers created by the application
state['loggers'] = {}

state['root_logger'] = None
state['log'] = None

# global verbosity levels (used for loggers for which an explicit level is not set)
state['verbosity'] = 0
state['log_verbosity'] = None

state['subprocess_label'] = None
state['parent_process'] = psutil.Process(os.getpid())
state['log_memory_totals'] = True
state['log_memory_types'] = None, "rss vms".split(), "rss pss".split()
