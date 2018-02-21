#!/usr/bin/python3
# -*- coding: utf-8 -*-

import functools
import signal


class TimedOut(Exception):
    pass


def call_with_timeout(timeout, f, *args, **kwargs):
    """
    Call f with the given arguments, but if timeout seconds pass before
    f returns, raise TimedOut. The exception is raised asynchronously,
    so data structures being updated by f may be in an inconsistent state.

    """
    def handler(signum, frame):
        raise TimedOut("Timed out after {} seconds.".format(timeout))
    old = signal.signal(signal.SIGALRM, handler)
    try:
        signal.alarm(timeout)
        try:
            return f(*args, **kwargs)
        finally:
            signal.alarm(0)
    finally:
        signal.signal(signal.SIGALRM, old)


def with_timeout(timeout):
    """
    Decorator for a function that causes it to timeout after the given
    number of seconds.

    """
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            return call_with_timeout(timeout, f, *args, **kwargs)
        return wrapped
    return decorator
