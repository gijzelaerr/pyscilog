import os
import signal

from pyscilog import LogFilter


def _sigusr1_handler(signum, frame):
    level = 2 if LogFilter._log_memory == 1 else 1
    print("pid {} received USR1: memory logging level {}".format(os.getpid(), level))
    LogFilter.setMemoryLogging(level)


def _sigusr2_handler(signum, frame):
    print("pid {} received USR2: disabling memory logging".format(os.getpid()))
    LogFilter.setMemoryLogging(0)


def init_handlers():
    signal.signal(signal.SIGUSR1, _sigusr1_handler)
    signal.signal(signal.SIGUSR2, _sigusr2_handler)
