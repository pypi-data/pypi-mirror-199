# This file is placed in the Public Domain.


"messages"


import threading


from .objects import Object
from .default import Default
from .listens import Listens


def __dir__():
    return (
            'Message',
            'parse'
           )


__all__ = __dir__()


class Message(Default):

    __slots__ = ('_ready', '_thr')

    def __init__(self, *args, **kwargs):
        Default.__init__(self, *args, **kwargs)
        self._ready = threading.Event()
        self._thr = None
        self.args = []
        self.gets = Default()
        self.orig = None
        self.result = []
        self.sets = Default()
        self.skip = Default()

    def parse(self, txt):
        self.otxt = txt
        spl = self.otxt.split()
        args = []
        _nr = -1
        for word in spl:
            if word.startswith('-'):
                try:
                    self.index = int(word[1:])
                except ValueError:
                    self.opts = self.opts + word[1:2]
                continue
            try:
                key, value = word.split('==')
                if value.endswith('-'):
                    value = value[:-1]
                    setattr(self.skip, value, '')
                setattr(self.gets, key, value)
                continue
            except ValueError:
                pass
            try:
                key, value = word.split('=')
                setattr(self.sets, key, value)
                continue
            except ValueError:
                pass
            _nr += 1
            if _nr == 0:
                self.cmd = word
                continue
            args.append(word)
        if args:
            self.args = args
            self.rest = ' '.join(args)
            self.txt = self.cmd + ' ' + self.rest
        else:
            self.txt = self.cmd

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        for txt in self.result:
            Listens.say(self.orig, txt, self.channel)

    def wait(self):
        #if self._thr:
        #    self._thr.join()
        self._ready.wait()


def parse(txt):
    cfg = Message()
    cfg.parse(txt)
    if "v" in cfg.opts:
        cfg.verbose = True
    if "mod" in cfg.sets:
        cfg.mod = cfg.sets.mod
    return cfg
