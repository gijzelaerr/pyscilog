from dataclasses import dataclass
from pyscilog.state import State

SEPERATOR = "================================{}=================================="


@dataclass
class ColorMap:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    NOBOLD = '\033[0m'


color_dict = dict(red=ColorMap.FAIL, green=ColorMap.OKGREEN, yellow=ColorMap.WARNING, blue=ColorMap.OKBLUE, white="")

state = State()


def cprint(string: str, col="red", bold=True):
    if state['silent']:
        return string

    ss = color_dict.get(col)
    if ss is None:
        raise ValueError("unknown color '{}'".format(col))

    ss = "%s%s%s" % (ss, string, ColorMap.ENDC)
    if bold:
        ss = "%s%s%s" % (ColorMap.BOLD, ss, ColorMap.NOBOLD)

    return ss


def disable_colors():
    state.silent = True


def separate(strin=None, D=1):
    if D != 1:
        return cprint(SEPERATOR.format("=" * len(strin)))
    else:
        return cprint(SEPERATOR.format(strin))


def title(strin, big=False):
    print()
    print()
    if big:
        print(separate(strin, D=0))

    print(separate(strin))

    if big:
        print(separate(strin, D=0))

    print()


def disable():
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
