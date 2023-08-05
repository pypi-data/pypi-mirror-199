# This file is placed in the Public Domain.


import unittest


from operbot.decoder import loads
from operbot.encoder import dumps
from operbot.objects import Object


class TestDecoder(unittest.TestCase):

    def test_loads(self):
        obj = Object()
        obj.test = 'bla'
        oobj = loads(dumps(obj))
        self.assertEqual(oobj.test, 'bla')

