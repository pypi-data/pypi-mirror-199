# This file is placed in the Public Domain.


'handler'


import queue
import threading


from .command import Command
from .objects import Object, update
from .message import Message
from .threads import launch


def __dir__():
    return (
            'Handler',
           )


__all__ = __dir__()


class Handler(Object):

    errors = []

    def __init__(self):
        Object.__init__(self)
        self.cbs = Object()
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        self.register('command', self.handle)

    def clone(self, other):
        update(self.cmds, other.cmds)

    def dispatch(self, func, evt):
        try:
            func(evt)
        except Exception as ex:
            exc = ex.with_traceback(ex.__traceback__)
            Handler.errors.append(exc)

    def event(self, txt):
        msg = Message()
        msg.orig = repr(self)
        msg.type = 'command'
        msg.txt = txt
        return msg

    def handle(self, evt):
        func = getattr(self.cbs, evt.type, None)
        if func:
            evt._thr = launch(self.dispatch, func, evt)
        return evt

    def loop(self):
        while not self.stopped.set():
            self.handle(self.poll())

    def poll(self):
        return self.queue.get()

    def put(self, evt):
        self.queue.put_nowait(evt)

    def register(self, cmd, func):
        setattr(self.cbs, cmd, func)

    def stop(self):
        self.stopped.set()
