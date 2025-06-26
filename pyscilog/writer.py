from pyscilog import cprint
from typing import Set, Any


class Writer:
    """A default writer logs messages to a logger"""
    __print_once_keys: Set[Any] = set()

    def __init__(self, logger, level, color=None, bold=None):
        self.logger = logger
        self.level = level
        self.color = (color or "red") if bold else color
        self.bold = bool(color) if bold is None else bold

    def write(self, message, level_override=None, print_once: Any = None):
        if print_once is not None:
            if print_once in Writer.__print_once_keys:
                return
            current_keys = Writer.__print_once_keys
            Writer.__print_once_keys = set(current_keys.union(set(print_once)))

        message = message.rstrip()
        # do not colorize empty messages, else "\n" is issued independently
        if self.color and message:
            message = cprint(message, col=self.color, bold=self.bold)
        level = self.level if level_override is None else level_override
        self.logger.log(level, message)

    def print(self, *args):
        return self.write(" ".join(map(str, args)))
