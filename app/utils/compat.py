"""
Cross-platform compatibility module for threading

Uses standard threading on all platforms for reliability.
Eventlet is deprecated and has compatibility issues with Python 3.13+.

This module provides a simple, consistent API for background tasks.
"""

import platform
import time as _time
import threading

IS_WINDOWS = platform.system() == 'Windows'


def sleep(seconds):
    """Sleep for specified seconds"""
    _time.sleep(seconds)


def spawn(func, *args, **kwargs):
    """Spawn a background task as a daemon thread"""
    thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    return ThreadWrapper(thread)


def create_lock():
    """Create a lock for thread synchronization"""
    return threading.Lock()


class ThreadWrapper:
    """Wrapper to provide a consistent interface for threads"""
    def __init__(self, thread):
        self.thread = thread
        self._dead = False

    @property
    def dead(self):
        return not self.thread.is_alive()

    def is_alive(self):
        return self.thread.is_alive()

    def wait(self, timeout=None):
        """Wait for thread to complete"""
        self.thread.join(timeout=timeout)

    def join(self, timeout=None):
        """Alias for wait()"""
        self.thread.join(timeout=timeout)

    def kill(self):
        """Cannot actually kill a thread, just mark as dead"""
        self._dead = True


def spawn_n(func, *args, **kwargs):
    """Spawn without returning handle (fire and forget)"""
    thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
    thread.start()
