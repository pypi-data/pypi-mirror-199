# This file is placed in the Public Domain.


"a clean namespace"


def __dir__():
    return (
            'Object',
            'items',
            'keys',
            'kind',
            'update',
            'values'
            )


__all__ = __dir__()


class Object:


    def __init__(self, *args, **kwargs):
        ""
        if args:
            val = args[0]
            if isinstance(val, list):
                update(self, dict(val))
            elif isinstance(val, zip):
                update(self, dict(val))
            elif isinstance(val, dict):
                update(self, val)
            elif isinstance(val, Object):
                update(self, vars(val))
        if kwargs:
            self.__dict__.update(kwargs)

    def __iter__(self):
        ""
        return iter(self.__dict__)

    def __len__(self):
        ""
        return len(self.__dict__)

    def __str__(self):
        ""
        return str(self.__dict__)


def items(obj):
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    return obj.__dict__.keys()


def kind(obj):
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = obj.__name__
    return kin


def update(obj, data):
    for key, value in items(data):
        setattr(obj, key, value)


def values(obj):
    return obj.__dict__.values()
