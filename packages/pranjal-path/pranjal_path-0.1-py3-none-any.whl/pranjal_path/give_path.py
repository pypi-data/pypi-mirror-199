import os


def directory_name():
    here = os.path.abspath(os.path.dirname(__file__))
    return here
    