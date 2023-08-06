r"""
A.N. 202206
---
general utils.
"""
import datetime
import logging
import os
import sys
import time
import warnings
from importlib import reload
from types import ModuleType

from getkey import getkey


def rreload(module, max_depth, depth=0):
    """Recursively reload modules."""
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if type(attribute) is ModuleType:
            if depth < max_depth:
                rreload(attribute, max_depth, depth + 1)
    reload(module)


def flatten(lst: list) -> list:
    r"""
    flattens a list of lists or tuples.
    """
    ret = []
    for item in lst:
        if isinstance(item, (list, tuple)):
            ret += flatten(item)
        else:
            ret.append(item)
    return ret


def get_user_choice(prompt: str = 'please confirm', choices: list = None) -> str:
    r"""
    get **one** character from input
    """
    if choices is None:
        choices = ['y', 'n']
    while True:
        if not (prompt.endswith(':') or prompt.endswith(': ')):
            prompt += ':'
        print(f'{prompt} -> [{"/".join(choices)}] ', end='')
        sys.stdout.flush()
        key = getkey()
        print(key, end='')
        if key in choices:
            print()
            break
        else:
            print(' invalid input. ')
            continue
    return key


def print_with_time(*args, **kwargs):
    r"""print with time.
    """
    print(f'[{str(datetime.datetime.now())}]', end=' ')
    print(*args, **kwargs)
    sys.stdout.flush()


def silent(mode='all'):
    r"""silent a function.
    params:
        mode: 'all', 'err', 'warn' or 'out'
    """

    def silencer(fn):

        def wrapped(*args, **kwargs):
            oo, oe = sys.stdout, sys.stderr
            with open(os.devnull, 'w', encoding='utf-8') as devnull:
                if mode == 'out':
                    sys.stdout = devnull
                    ret = fn(*args, **kwargs)
                    sys.stdout = oo
                elif mode == 'err':
                    sys.stderr = devnull
                    ret = fn(*args, **kwargs)
                    sys.stderr = oo
                elif mode == 'all':
                    sys.stdout = devnull
                    sys.stderr = devnull
                    ret = fn(*args, **kwargs)
                    sys.stdout, sys.stderr = oo, oe
                elif mode == 'warn':
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore')
                        ret = fn(*args, **kwargs)
                else:
                    raise (ValueError("mode should be in ['out', 'err', 'all', 'warn']"))
            return ret

        return wrapped

    return silencer


def timing(fn, show_datetime: bool = True):
    r"""time a function.
    """

    def timed(*args, **kwargs):
        start = time.time()
        ret = fn(*args, **kwargs)
        tmstr = "{} elapse: {:.3f} s".format(fn.__name__, time.time() - start)
        if show_datetime:
            tmstr = ' '.join(['[' + str(datetime.datetime.now()) + ']', tmstr])
        print(tmstr)
        return ret

    return timed


def logging_to(target_dir: str, need_timing_in_name: bool = False):
    r"""log a function to a file.
    """
    assert os.path.isdir(target_dir)

    def decorator(fn):

        def logged_fn(*args, **kwargs):
            if need_timing_in_name:
                dt = datetime.datetime.now()
                txt_path = os.path.join(
                    target_dir,
                    "log_{:d}_{:d}_{:d}_{:d}_{:d}_{:d}.txt".format(dt.year, dt.month, dt.day,
                                                                   dt.hour, dt.minute,
                                                                   dt.second))
            else:
                txt_path = os.path.join(target_dir, 'log.txt')

            with open(txt_path, 'w', encoding='utf-8') as f:
                old_stdout = sys.stdout
                sys.stdout = f
                ret = fn(*args, **kwargs)
                sys.stdout = old_stdout
            return ret

        return logged_fn

    return decorator


def get_datetime_str() -> str:
    r"""get datetime str.
    """
    dt = datetime.datetime.now()
    dt_str = "{:d}_{:d}_{:d}_{:d}_{:d}_{:d}".format(dt.year, dt.month, dt.day, dt.hour,
                                                    dt.minute, dt.second)
    return dt_str


def create_logger(name='', ch=True, fh=None, levelname=logging.INFO, overwrite=False):
    # Author: Xiong Lei
    logger = logging.getLogger(name)
    logger.setLevel(levelname)

    if overwrite:
        for h in logger.handlers:
            logger.removeHandler(h)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # handler
    if ch:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    if fh is not None:
        fh = logging.FileHandler(fh, mode='w')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


class Tee(object):
    """
    https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file/616686#616686
    """

    def __init__(self, source, name, mode):
        assert source in ['o', 'e']
        self.source = source
        self.file = open(name, mode)
        if 'o' in source:
            self.stdout = sys.stdout
            sys.stdout = self
        elif 'e' in source:
            self.stderr = sys.stderr
            sys.stderr = self

    def __del__(self):
        self.flush()
        if 'o' in self.source:
            sys.stdout = self.stdout
        elif 'e' in self.source:
            sys.stderr = self.stderr
        self.file.close()

    def write(self, data):
        self.file.write(data)
        if 'o' in self.source:
            self.stdout.write(data)
        elif 'e' in self.source:
            self.stderr.write(data)

    def flush(self):
        self.file.flush()
        if 'o' in self.source:
            self.stdout.flush()
        elif 'e' in self.source:
            self.stderr.flush()