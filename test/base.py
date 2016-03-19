import unittest

import jsonschema


class SchemaTestCase(unittest.TestCase):
    def assertSchema(self, actual, expected):
        self.assertValidSchema(actual)
        self.assertEqual(actual, expected)

    def assertValidSchema(self, schema):
        jsonschema.Draft4Validator.check_schema(schema)
