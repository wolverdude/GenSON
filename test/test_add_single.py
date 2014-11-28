import unittest
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from jschemagen import Schema


class TestType(unittest.TestCase):

    def test_no_schema(self):
        schema = {}
        s = Schema()
        s.add_schema(schema)
        self.assertEqual(s.to_dict(), schema)

    def test_single_type(self):
        schema = {'type': 'string'}
        s = Schema()
        s.add_schema(schema)
        self.assertEqual(s.to_dict(), schema)

    def test_single_type_unicode(self):
        schema = {u'type': u'string'}
        s = Schema()
        s.add_schema(schema)
        self.assertEqual(s.to_dict(), schema)

    def test_multi_type(self):
        schema = {'type': ['boolean', 'null', 'number', 'string']}
        s = Schema()
        s.add_schema(schema)
        self.assertEqual(s.to_dict(), schema)


class TestPreserveKeys(unittest.TestCase):

    def test_preserves_existing_keys(self):
        schema = {'type': 'number', 'value': 5}
        s = Schema()
        s.add_schema(schema)
        self.assertEqual(s.to_dict(), schema)


if __name__ == '__main__':
    unittest.main()
