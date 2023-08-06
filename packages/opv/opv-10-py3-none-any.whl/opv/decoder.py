# This file is placed in the Public Domain.
# pylint: disable=C0112,C0115,C0116


"json decoder"


import json


from json import JSONDecoder


from .objects import Object, update


def __dir__():
    return (
            'ObjectDecoder',
            'load',
            'loads',
            'read'
           )


__all__ = __dir__()


class ObjectDecoder(JSONDecoder):

    errors = []

    def __init__(self):
        ""
        JSONDecoder.__init__(self)

    def decode(self, s, _w=None) -> Object:
        ""
        val = JSONDecoder.decode(self, s)
        if not val:
            val = {}
        return Object(val)

    def raw_decode(self, s, idx=0) -> (int, Object):
        ""
        return JSONDecoder.raw_decode(self, s, idx)


def load(fpt, *args, **kw) -> Object:
    return json.load(fpt, *args, cls=ObjectDecoder, **kw)


def loads(string, *args, **kw) -> Object:
    return json.loads(string, *args, cls=ObjectDecoder, **kw)


def read(obj, path) -> None:
    with open(path, 'r', encoding='utf-8') as ofile:
        data = load(ofile)
        update(obj, data)
