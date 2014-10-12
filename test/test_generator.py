import unittest
import os
import sys
from schemagen import SchemaGen

sys.path.insert(1, os.path.join(sys.path[0], '..'))


class TestPrimaryTypes(unittest.TestCase):

    def test_no_object(self):
        sg = SchemaGen()
        self.assertEqual(sg.get_schema(), {})

    def test_string(self):
        sg = SchemaGen().add_object('string')
        self.assertEqual(sg.get_schema(), {'type': 'string'})

    def test_number(self):
        sg = SchemaGen().add_object(1.1)
        self.assertEqual(sg.get_schema(), {'type': 'number'})

    def test_boolean(self):
        sg = SchemaGen().add_object(True)
        self.assertEqual(sg.get_schema(), {'type': 'boolean'})

    def test_null(self):
        sg = SchemaGen().add_object(None)
        self.assertEqual(sg.get_schema(), {'type': 'null'})


class TestArray(unittest.TestCase):

    def test_empty(self):
        sg = SchemaGen().add_object([])
        self.assertEqual(sg.get_schema(),
                         {'type': 'array', 'items': []})

    def test_monotype(self):
        sg = SchemaGen().add_object(['spam', 'spam', 'eggs', 'spam'])
        self.assertEqual(sg.get_schema(),
                         {'type': 'array', 'items': [{'type': 'string'}]})

    def test_multitype(self):
        sg = SchemaGen().add_object([1, '2', None, False])
        self.assertEqual(sg.get_schema(), {
            'type': 'array',
            'items': [
                {'type': 'number'},
                {'type': 'string'},
                {'type': 'null'},
                {'type': 'boolean'}]})


class TestObject(unittest.TestCase):

    def test_empty_object(self):
        sg = SchemaGen().add_object({})
        self.assertEqual(sg.get_schema(),
                         {'required': [], 'type': 'object', 'properties': {}})

    def test_basic_object(self):
        sg = SchemaGen().add_object({
            'Red Windsor': 'Normally, but today the van broke down.',
            'Stilton': 'Sorry.',
            'Gruyere': False})
        self.assertEqual(sg.get_schema(), {
            'required': ['Gruyere', 'Red Windsor', 'Stilton'],
            'type': 'object',
            'properties': {
                'Red Windsor': {'type': 'string'},
                'Gruyere': {'type': 'boolean'},
                'Stilton': {'type': 'string'}}})


if __name__ == '__main__':
    unittest.main()
