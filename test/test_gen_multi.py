import unittest
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from genson import Schema
import base


class TestBasicTypes(base.SchemaTestCase):

    def test_single_type(self):
        s = Schema()
        s.add_object('bacon')
        s.add_object('egg')
        s.add_object('spam')
        self.assertSchema(s.to_dict(), {'type': 'string'})

    def test_multi_type(self):
        s = Schema()
        s.add_object('string')
        s.add_object(1.1)
        s.add_object(True)
        s.add_object(None)
        self.assertSchema(s.to_dict(),
                          {'type': ['boolean', 'null', 'number', 'string']})

    def test_redundant_integer_type(self):
        s = Schema()
        s.add_object(1)
        s.add_object(1.1)
        self.assertSchema(s.to_dict(),
                          {'type': 'number'})


if __name__ == '__main__':
    unittest.main()
