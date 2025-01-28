import sys
import unittest
import jsonschema
from genson import SchemaNode, SchemaBuilder
from .sort import sort_lists_in_schema, Py2Key

PYTHON_VERSION = sys.version[:sys.version.find(' ')]


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.builder = self.CLASS()
        self._objects = []
        self._schemas = []

    def set_schema_options(self, **options):
        self.builder = SchemaNode(**options)

    def add_object(self, obj):
        self.builder.add_object(obj)
        self._objects.append(obj)

    def add_schema(self, schema):
        self.builder.add_schema(schema)
        self._schemas.append(schema)

    def assertObjectValidates(self, obj):
        jsonschema.Draft7Validator(self.builder.to_schema()).validate(obj)

    def assertObjectDoesNotValidate(self, obj):
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.Draft7Validator(self.builder.to_schema()).validate(obj)

    def assertResult(self, expected, enforceUserContract=True, ignore_order=False):
        actual = self.builder.to_schema()
        if ignore_order:
            sort_lists_in_schema(actual, Py2Key)
            sort_lists_in_schema(expected, Py2Key)
        self.assertEqual(
            expected, actual, 
            'Generated schema (below) does not match expected (above)')
        if enforceUserContract:
            self.assertUserContract()

    def assertUserContract(self):
        self._assertSchemaIsValid()
        self._assertComponentObjectsValidate()

    def _assertSchemaIsValid(self):
        jsonschema.Draft7Validator.check_schema(self.builder.to_schema())

    def _assertComponentObjectsValidate(self):
        compiled_schema = self.builder.to_schema()
        for obj in self._objects:
            jsonschema.Draft7Validator(compiled_schema).validate(obj)


class SchemaNodeTestCase(BaseTestCase):
    CLASS = SchemaNode


class SchemaBuilderTestCase(BaseTestCase):
    CLASS = SchemaBuilder
