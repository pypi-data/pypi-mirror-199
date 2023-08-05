# This file is placed in the Public Domain.


"json decoding"


import json
import _thread


from .objects import Object
from .utility import locked


def __dir__():
    return (
            'ObjectDecoder',
            'load',
            'loads',
           )


__all__ = __dir__()


jsonlock = _thread.allocate_lock()


class ObjectDecoder(json.JSONDecoder):

    def decode(self, s, _w=None):
        if s == "":
            val = {}
        else:
            val = json.loads(s)
        return Object(val)

    def raw_decode(self, s, idx=0):
        return json.JSONDecoder.raw_decode(self, s, idx)


def load(
         fnm,
         *args,
         cls=None,
         object_hook=None,
         parse_float=None,
         parse_int=None,
         parse_constant=None,
         object_pairs_hook=None,
         **kw
        ):
    return json.load(
                     fnm,
                     *args,
                     cls=ObjectDecoder,
                     parse_float=parse_float,
                     parse_int=parse_int,
                     parse_constant=parse_constant,
                     object_pairs_hook=object_pairs_hook,
                     **kw
                    )

def loads(
          s,
          *args,
          cls=None,
          object_hook=None,
          parse_float=None,
          parse_int=None,
          parse_constant=None,
          object_pairs_hook=None,
          **kw
         ):
    return json.loads(
                      s,
                      *args,
                      cls=ObjectDecoder,
                      parse_float=parse_float,
                      parse_int=parse_int,
                      parse_constant=parse_constant,
                      object_pairs_hook=object_pairs_hook,
                      **kw
                     )
