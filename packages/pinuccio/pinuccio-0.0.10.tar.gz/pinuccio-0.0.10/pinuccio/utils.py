from __future__ import print_function

DEBUG = True
ERROR = True
INFO = True


def debug(*args):
    if DEBUG:
        print("[DEBUG]",*args)

def info(*args):
    if info:
        print("[INFO]",*args)

def error(*args):
    if ERROR:
        print("[ERROR]",*args)


