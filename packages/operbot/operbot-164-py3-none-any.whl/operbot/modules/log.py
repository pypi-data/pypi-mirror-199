# This file is placed in the Public Domain.


'log'


import time


from ..objects import Object
from ..storage import Storage, find, save
from ..utility import elapsed, fntime


def __dir__():
    return (
            'Log',
            'log',
           )


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


Storage.add(Log)


def log(event):
    if not event.rest:
        nmr = 0
        for fnm, obj in find('log'):
            event.reply('%s %s %s' % (
                                      nmr,
                                      obj.txt,
                                      elapsed(time.time() - fntime(fnm)))
                                     )
            nmr += 1
        if not nmr:
            event.reply('log <txt>')
        return
    obj = Log()
    obj.txt = event.rest
    save(obj)
    event.reply('ok')
