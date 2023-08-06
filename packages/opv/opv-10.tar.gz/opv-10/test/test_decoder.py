# This file is placed in the Public Domain.


import unittest


from opv import Object
from opv.decoder import loads
from opv.encoder import dumps


class TestDecoder(unittest.TestCase):

    def test_loads(self):
        obj = Object()
        obj.test = "bla"
        oobj = loads(dumps(obj))
        self.assertEqual(oobj.test, "bla")

