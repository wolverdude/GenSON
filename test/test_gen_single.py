import unittest
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from jschemagen import Schema


class TestBasicTypes(unittest.TestCase):

    def test_no_object(self):
        s = Schema()
        self.assertEqual(s.to_dict(), {})

    def test_string(self):
        s = Schema().add_object('string')
        self.assertEqual(s.to_dict(), {'type': 'string'})

    def test_number(self):
        s = Schema().add_object(1.1)
        self.assertEqual(s.to_dict(), {'type': 'number'})

    def test_boolean(self):
        s = Schema().add_object(True)
        self.assertEqual(s.to_dict(), {'type': 'boolean'})

    def test_null(self):
        s = Schema().add_object(None)
        self.assertEqual(s.to_dict(), {'type': 'null'})


class TestArray(unittest.TestCase):

    def test_empty(self):
        s = Schema().add_object([])
        self.assertEqual(s.to_dict(),
                         {'type': 'array', 'items': []})

    def test_monotype(self):
        s = Schema().add_object(['spam', 'spam', 'spam', 'egg', 'spam'])
        self.assertEqual(s.to_dict(),
                         {'type': 'array', 'items': [{'type': 'string'}]})

    def test_multitype(self):
        s = Schema().add_object([1, '2', None, False])
        self.assertEqual(s.to_dict(), {
            'type': 'array',
            'items': [
                {'type': 'number'},
                {'type': 'string'},
                {'type': 'null'},
                {'type': 'boolean'}]
            })


class TestObject(unittest.TestCase):

    def test_empty_object(self):
        s = Schema().add_object({})
        self.assertEqual(s.to_dict(), {'type': 'object', 'properties': {}})

    def test_basic_object(self):
        s = Schema().add_object({
            'Red Windsor': 'Normally, but today the van broke down.',
            'Stilton': 'Sorry.',
            'Gruyere': False})
        self.assertEqual(s.to_dict(), {
            'required': ['Gruyere', 'Red Windsor', 'Stilton'],
            'type': 'object',
            'properties': {
                'Red Windsor': {'type': 'string'},
                'Gruyere': {'type': 'boolean'},
                'Stilton': {'type': 'string'}}
            })


class TestComplex(unittest.TestCase):

    def test_array_reduce(self):
        s = Schema().add_object([['egg', 'spam'],
                                     ['egg', 'bacon', 'spam'],
                                     ['egg', 'bacon', 'sausage', 'spam'],
                                     ['spam', 'bacon', 'sausage', 'spam']])
        self.assertEqual(s.to_dict(), {
            'type': 'array',
            'items': [{
                'type': 'array',
                'items': [{'type': 'string'}]}]
            })

    def test_array_in_object(self):
        pass

    def test_object_in_array(self):
        pass

    def test_three_deep(self):
        pass


if __name__ == '__main__':
    unittest.main()
