import unittest
from . import base


class TestBasicTypes(base.SchemaTestCase):

    def test_single_type(self):
        self.add_object('bacon')
        self.add_object('egg')
        self.add_object('spam')
        self.assertResult({'type': 'string'})

    def test_multi_type(self):
        self.add_object('string')
        self.add_object(1.1)
        self.add_object(True)
        self.add_object(None)
        self.assertResult({'type': ['boolean', 'null', 'number', 'string']})

    def test_redundant_integer_type(self):
        self.add_object(1)
        self.add_object(1.1)
        self.assertResult({'type': 'number'})
