import sys
import unittest

try:
    import jsonschema
except ImportError:
    print('Failed to import jsonschema module. Schemas will not be validated.')


class SchemaTestCase(unittest.TestCase):
    def assertSchema(self, actual, expected):
        self.assertValidSchema(actual)
        self.assertEqual(actual, expected)

    def assertValidSchema(self, schema):
        if 'jsonschema' in sys.modules:
            jsonschema.Draft4Validator.check_schema(schema)
