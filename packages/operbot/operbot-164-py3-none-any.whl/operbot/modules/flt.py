# This file is placed in the Public Domain.


"list of bots"


from ..listens import Listens


def __dir__():
    return (
            'flt',
           )


__all__ = __dir__()


def flt(event):
    try:
        index = int(event.args[0])
        event.reply(Listens.objs[index])
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(' | '.join([o.__type__() for o in Listens.objs]))
