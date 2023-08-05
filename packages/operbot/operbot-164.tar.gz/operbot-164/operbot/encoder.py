# This file is placed in the Public Domain.


"json encoding"


import json


from .decoder import jsonlock
from .objects import Object
from .utility import locked


def __dir__():
    return (
            'ObjectEncoder',
            'dump',
            'dumps'
           )


__all__ = __dir__()



class ObjectEncoder(json.JSONEncoder):


    def default(self, o):
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(o,
                      (type(str), type(True), type(False),
                       type(int), type(float))
                     ):
            return str(o)
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return str(o)


@locked(jsonlock)
def dump(
         obj,
         fnm,
         *args,
         skipkeys=False,
         ensure_ascii=True,
         check_circular=True,
         allow_nan=True,
         cls=None,
         indent=None,
         separators=None,
         default=None,
         sort_keys=False,
         **kw
        ):
    return json.dump(
                     obj,
                     fnm,
                     *args,
                     skipkeys=skipkeys,
                     ensure_ascii=ensure_ascii,
                     check_circular=check_circular,
                     allow_nan=allow_nan,
                     cls=ObjectEncoder,
                     indent=indent,
                     separators=separators,
                     default=default,
                     sort_keys=sort_keys,
                     **kw
                    )



@locked(jsonlock)
def dumps(
          obj,
          *args,
          skipkeys=False,
          ensure_ascii=True,
          check_circular=True,
          allow_nan=True,
          cls=None,
          indent=None,
          separators=None,
          default=None,
          sort_keys=False,
          **kw
         ):
    return json.dumps(
                      obj,
                      *args,
                      skipkeys=skipkeys,
                      ensure_ascii=ensure_ascii,
                      check_circular=check_circular,
                      allow_nan=allow_nan,
                      cls=ObjectEncoder,
                      indent=indent,
                      separators=separators,
                      default=default,
                      sort_keys=sort_keys,
                      **kw
                     )
