# This file is placed in the Public Domain.


'status'


import io
import traceback


from ..generic import format
from ..handler import Handler
from ..listens import Listens


def err(event):
    for ex in Handler.errors:
        stream = io.StringIO(traceback.print_exception(type(ex), ex, ex.__traceback__))
        for line in stream.readlines():
            event.reply(line)


def sts(event):
    for bot in Listens.objs:
        if 'state' in dir(bot):
            event.reply(format(bot.state, skip='lastline'))
