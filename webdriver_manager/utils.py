import platform
import sys


def os_name():
    pl = sys.platform
    if pl == "linux" or pl == "linux2":
        return "linux"
    elif pl == "darwin":
        return "mac"
    elif pl == "win32":
        return "win"


def os_architecture():
    bits = platform.architecture()[0]
    if bits == "64bit":
        return 64
    return 32


def os_type():
    return os_name() + str(os_architecture())
