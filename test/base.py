import unittest
import jsonschema
import os, sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from genson import Schema, SchemaError

class SchemaTestCase(unittest.TestCase):

    def assertGenSchema(self, instance, options, expected):
        actual = Schema(**options).add_object(instance).to_dict()
        self.assertSchema(actual, expected)
        self.assertValidData(instance, actual)
        return actual

    def assertSchema(self, actual, expected):
        self.assertValidSchema(actual)
        self.assertEqual(actual, expected)

    def assertValidSchema(self, schema):
        jsonschema.Draft4Validator.check_schema(schema)

    def assertValidData(self, data, schema):
        jsonschema.Draft4Validator(schema).validate(data)

    def assertInvalidData(self, data, schema):
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.Draft4Validator(schema).validate(data)
