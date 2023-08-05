# This file is placed in the Public Domain.


'todo'


import time


from ..objects import Object
from ..storage import Storage, find, save
from ..utility import elapsed, fntime


class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


Storage.add(Todo)


def dne(event):
    if not event.args:
        return
    selector = {'txt': event.args[0]}
    for fnm, o in find('todo', selector):
        o.__deleted__ = True
        save(o, fnm)
        event.reply('ok')
        break


def tdo(event):
    if not event.rest:
        nr = 0
        for _fn, o in find('todo'):
            event.reply('%s %s %s' % (nr, o.txt, elapsed(time.time() - fntime(_fn))))
            nr += 1
        if not nr:
            event.reply("nothing todo")
        return
    o = Todo()
    o.txt = event.rest
    save(o)
    event.reply('ok')
