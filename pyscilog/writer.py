from pyscilog import cprint
from typing import Set, Any


class Writer:
    """A default writer logs messages to a logger"""
    __print_once_keys: Set[Any] = []

    def __init__(self, logger, level, color=None, bold=None):
        self.logger = logger
        self.level = level
        self.color = (color or "red") if bold else color
        self.bold = bool(color) if bold is None else bold

    def write(self, message, level_override=None, print_once: Any = None):
        if print_once is not None:
            if print_once in Writer.__print_once_keys:
                return
            Writer.__print_once_keys = set(Writer.__print_once_keys.union(set(print_once)))

        message = message.rstrip()
        if self.color and message:  # do not colorize empty messages, else "\n" is issued independently
            message = cprint(message, col=self.color, bold=self.bold)
        self.logger.log(self.level if level_override is None else level_override, message)

    def print(self, *args):
        return self.write(" ".join(map(str, args)))
