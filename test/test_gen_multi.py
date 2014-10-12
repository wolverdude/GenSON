import unittest
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from schemagen import SchemaGen


class TestBasicTypes(unittest.TestCase):

    def test_single_type(self):
        sg = SchemaGen()
        sg.add_object('bacon')
        sg.add_object('egg')
        sg.add_object('spam')
        self.assertEqual(sg.get_schema(), {'type': 'string'})

    def test_multi_type(self):
        sg = SchemaGen()
        sg.add_object('string')
        sg.add_object(1.1)
        sg.add_object(True)
        sg.add_object(None)
        self.assertEqual(sg.get_schema(),
                         {'type': ['boolean', 'null', 'number', 'string']})


if __name__ == '__main__':
    unittest.main()
