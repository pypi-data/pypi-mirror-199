# This file is placed in the Public Domain.


"a clean namespace"


from .decoder import read
from .encoder import write
from .objects import Object, items, keys, kind, update, values


def __dir__():
    return (
            'Object',
            'items',
            'keys',
            'kind',
            'read',
            'update',
            'values',
            'write'
           )


__all__ = __dir__()
         