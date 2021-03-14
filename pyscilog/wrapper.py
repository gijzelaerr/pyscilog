import logging
import sys
from re import sub
from pyscilog.filter import LogFilter
from pyscilog.writer import Writer
from pyscilog.state import State

state = State()
log_filter = LogFilter()
fmt = "%(asctime)s - %(shortname)-18.18s %(subprocess)s%(memory)s%(separator)s%(message)s"
datefmt = '%H:%M:%S'  # '%H:%M:%S.%f'

# this will be a null handler
null_handler = logging.NullHandler()


class ColorStrippingFormatter(logging.Formatter):
    def __init__(self, fmt, datefmt, strip=True):
        logging.Formatter.__init__(self, fmt, datefmt)
        self.strip = strip

    def label(self, record):
        if record.levelno < logging.WARNING:
            return "INFO", "37;42"
        elif record.levelno < logging.ERROR:
            return "WARNING", "37;43"
        elif record.levelno < logging.CRITICAL:
            return "ERROR", "5;41"
        else:
            return "CRITICAL", "5;41"

    def format(self, record):
        """Uses parent class to format record, then strips off colors"""
        msg = logging.Formatter.format(self, record)
        label, color = self.label(record)
        if self.strip:
            return "{:10s}{}".format(label, sub("\033\\[[0-9]+m", "", msg, 0))
        else:
            return "\033[1;{}m{:10s}\033[0m{}".format(color, label, msg)


_logfile_formatter = ColorStrippingFormatter(fmt, datefmt, strip=True)
_console_formatter = ColorStrippingFormatter(fmt, datefmt, strip=False)


class LoggerWrapper:
    def __init__(self, logger, verbose=None, log_verbose=None):
        self.logger = logger
        logger.propagate = False

        self.console_handler = logging.StreamHandler(sys.stderr)
        self.console_handler.setFormatter(_console_formatter)

        self.logfile_handler = logging.handlers.MemoryHandler(1, logging.DEBUG, state['file_handler'] or null_handler)
        self.logfile_handler.setFormatter(_logfile_formatter)

        # set verbosity levels
        self._verbose = self._log_verbose = None
        self.verbosity(verbose if verbose is not None else state['verbosity'])
        self.log_verbosity(log_verbose if log_verbose is not None else state['log_verbosity'])

        # other init
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.logfile_handler)
        self.logger.addFilter(log_filter)

    def verbosity(self, set_verb=None):
        if set_verb is not None:
            self._verbose = set_verb
            self.console_handler.setLevel(logging.INFO - set_verb)
            if self._log_verbose is None:
                self.logfile_handler.setLevel(logging.INFO - set_verb)
        return self._verbose

    def log_verbosity(self, set_verb=None):
        if set_verb is not None:
            self._log_verbose = set_verb
            self.logfile_handler.setLevel(logging.INFO - set_verb)
        return self._log_verbose if self._log_verbose is not None else self._verbose

    def __call__(self, level, color=None):
        """
        Function call operator on logger. Use to issue messages at different verbosity levels.
        E.g. log(2).print("message" will issue a message at level logging.INFO - 2.)
        An optional color argument will colorize the message.
        Returns:
            A writer object (to which a message may be sent with "<<")
        """
        # effective verbosity level is either set explicitly when the writer is created, or else use global level
        return Writer(self.logger, logging.INFO - level, color=color)

    def warn(self, msg, color=None, print_once=None):
        """
        Wrapper for log.warn
        """
        Writer(self.logger, logging.WARN, color=color).write(msg, print_once=print_once)

    warning = warn

    def error(self, msg, color="red", print_once=None):
        """
        Wrapper for log.error
        """
        Writer(self.logger, logging.ERROR, color=color).write(msg, print_once=print_once)

    def info(self, msg, color=None, print_once=None):
        """
        Wrapper for log.info
        """
        Writer(self.logger, logging.INFO, color=color).write(msg, print_once=print_once)

    def critical(self, msg, color=None, print_once=None):
        """
        Wrapper for log.critical
        """
        Writer(self.logger, logging.CRITICAL, color=color).write(msg, print_once=print_once)

    def debug(self, msg, color=None, print_once=None):
        """
        Wrapper for log.debug
        """
        Writer(self.logger, logging.DEBUG, color=color).write(msg, print_once=print_once)

    def exception(self, msg, color=None, print_once=None):
        """
        Wrapper for log.exception
        """
        Writer(self.logger, logging.EXCEPTION, color=color).write(msg, print_once=print_once)

    def print(self, *args):
        return self.info(" ".join(map(str, args)))

    def write(self, message, level=logging.INFO, verbosity=0, print_once=None, color=None):
        # apply verbosity only to INFO levels
        if level == logging.INFO:
            level -= int(verbosity)
        Writer(self.logger, level, color=color).write(message, print_once=print_once)


def log_to_file(filename, append=False):
    if not state['_file_handler']:
        _file_handler = logging.FileHandler(filename, mode='a' if append else 'w')
        _file_handler.setLevel(logging.DEBUG)
        _file_handler.setFormatter(_logfile_formatter)
        # set it as the target for the existing wrappers' handlers
        for wrapper in state['loggers'].values():
            wrapper.logfile_handler.setTarget(_file_handler)


def set_boring(boring=True):
    _console_formatter.strip = boring
