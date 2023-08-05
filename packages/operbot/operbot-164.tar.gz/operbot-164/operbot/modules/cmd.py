# This file is placed in the Public Domain.


'command'


from ..command import Command


def __dir__():
    return (
            'cmd',
           )


def cmd(event):
    event.reply(','.join(sorted(Command.cmds)))
