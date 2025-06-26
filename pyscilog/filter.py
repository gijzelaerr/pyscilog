import os
import time
from logging import Filter
import psutil
from multiprocessing import current_process
from pyscilog.color import cprint
from pyscilog.state import State

state = State()

GB = float(1024 ** 3)


def set_subprocess_label(label):
    """
    Sets the subprocess label explicitly
    """
    state['subprocess_label'] = label


def get_subprocess_label():
    """
    Returns the subprocess ID. For the main process, this is empty.
    For subprocesses (started by multiprocessing), this is "Pn" by default,
    where n is the process number.
    """
    if state['subprocess_label'] is None:
        name = current_process().name
        if name == "MainProcess":
            state['subprocess_label'] = ""
        else:
            state['subprocess_label'] = name.replace("Process-", "P")
    return state['subprocess_label']


class LogFilter(Filter):
    _log_memory = 0

    @staticmethod
    def setMemoryLogging(level):
        LogFilter._log_memory = level
        LogFilter._mem_ts = LogFilter._mem_totals_ts = 0
        LogFilter._children_ts = 0

    _mem = None
    _mem_totals = None
    _children = None
    _mem_ts = 0
    _mem_totals_ts = 0
    _children_ts = 0
    # full memory updates are costly, so do them only after seconds elapsed
    _mem_update = (0, .5, 2)
    _mem_totals_update = (0, 1, 5)
    # children updates even more so, so do it even less frequently
    _children_update = 3

    """LogFilter augments the event by a few new attributes used by our
    formatter"""

    def filter(self, event):
        if not event.getMessage().strip():
            return False
        # short logger name (without app_name in front of it)
        shortname = (event.name.split('.', 1)[1] if '.' in event.name
                     else event.name)
        setattr(event, 'shortname', shortname)
        setattr(event, 'separator', '| ')
        # signal handler can change that midway through, so use this value
        memlevel = LogFilter._log_memory
        if memlevel:
            # memory usage info
            t = time.time()
            if t - self._mem_ts > self._mem_update[memlevel]:
                keys = state['log_memory_types'][memlevel]
                # get memory for this process
                if memlevel == 2:
                    mi0 = psutil.Process(os.getpid()).memory_full_info()
                else:
                    mi0 = psutil.Process(os.getpid()).memory_info()
                mem = {key: getattr(mi0, key) / GB for key in keys}
                shm = psutil.virtual_memory().shared / GB
                # get total memory
                if state['log_memory_totals']:
                    totals_update = self._mem_totals_update[memlevel]
                    if t - self._mem_totals_ts > totals_update:
                        if t - self._children_ts > self._children_update:
                            parent = state['parent_process']
                            children = list(parent.children(recursive=True))
                            self._children = [parent] + children
                            self._children_ts = time.time()
                        if len(self._children) > 1:
                            mis = []
                            # scan over children, ignoring ones that may have
                            # disappeared
                            for p in self._children:
                                try:
                                    if memlevel == 2:
                                        mis.append(p.memory_full_info())
                                    else:
                                        mis.append(p.memory_info())
                                except psutil.NoSuchProcess:
                                    pass
                            totals = {}
                            for key in keys:
                                mem_sum = sum([getattr(mi, key) for mi in mis])
                                totals[key] = mem_sum / GB
                            self._mem_totals = totals
                        self._mem_totals_ts = time.time()
                # form up string
                if self._mem_totals is None:
                    smem = ["{:.1f}".format(mem.get(key, 0)) for key in keys]
                else:
                    fmt = "{:.1f}/{:.1f}"
                    smem = [fmt.format(mem.get(key, 0),
                                       self._mem_totals.get(key, 0))
                            for key in keys]
                smem.append("{:.1f}Gb".format(shm))
                self._mem = " ".join(smem)
                self._mem_ts = time.time()
            prefix = "*" if memlevel == 2 else ""
            memory_str = "[{}{}] ".format(prefix, self._mem)
            setattr(event, "memory", memory_str)
            setattr(event, 'separator', '')
        else:
            setattr(event, "memory", "")
        # subprocess info
        subprocess_id = get_subprocess_label()
        if subprocess_id:
            subprocess_str = cprint("[%s] " % subprocess_id, col="blue")
            setattr(event, "subprocess", subprocess_str)
            setattr(event, 'separator', '')
        else:
            setattr(event, "subprocess", "")
        return True
