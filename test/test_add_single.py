import unittest
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from schemagen import SchemaGen


class TestType(unittest.TestCase):

    def test_no_schema(self):
        schema = {}
        sg = SchemaGen(schema)
        self.assertEqual(sg.get_schema(), schema)

    def test_single_type(self):
        schema = {'type': 'string'}
        sg = SchemaGen(schema)
        self.assertEqual(sg.get_schema(), schema)

    def test_multi_type(self):
        schema = {'type': ['boolean', 'null', 'number', 'string']}
        sg = SchemaGen(schema)
        self.assertEqual(sg.get_schema(), schema)


class TestPreserveKeys(unittest.TestCase):

    def test_preserves_existing_keys(self):
        schema = {'type': 'number', 'value': 5}
        sg = SchemaGen(schema)
        self.assertEqual(sg.get_schema(), schema)


if __name__ == '__main__':
    unittest.main()
