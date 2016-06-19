import unittest
import jsonschema
from genson import Schema


class SchemaTestCase(unittest.TestCase):

    def setUp(self):
        self._schema = Schema()
        self._objects = []
        self._schemas = []

    def set_schema_options(self, **options):
        self._schema = Schema(**options)

    def add_object(self, obj):
        self._schema.add_object(obj)
        self._objects.append(obj)

    def add_schema(self, schema):
        self._schema.add_schema(schema)
        self._schemas.append(schema)

    def assertObjectValidates(self, obj):
        jsonschema.Draft4Validator(self._schema.to_dict()).validate(obj)

    def assertObjectDoesNotValidate(self, obj):
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.Draft4Validator(self._schema.to_dict()).validate(obj)

    def assertResult(self, expected):
        self.assertEqual(self._schema.to_dict(), expected)
        self.assertUserContract()

    def assertUserContract(self):
        self._assertSchemaIsValid()
        self._assertComponentObjectsValidate()

    def _assertSchemaIsValid(self):
        jsonschema.Draft4Validator.check_schema(self._schema.to_dict())

    def _assertComponentObjectsValidate(self):
        compiled_schema = self._schema.to_dict()
        for obj in self._objects:
            jsonschema.Draft4Validator(compiled_schema).validate(obj)
