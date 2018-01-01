from . import base
from genson import SchemaRoot


class TestParams(base.SchemaRootTestCase):

    def test_uri(self):
        test_uri = 'TEST_URI'
        self._schema = SchemaRoot(schema_uri=test_uri)
        self.assertResult({"$schema": test_uri})


class TestMethods(base.SchemaRootTestCase):

    def test_add_schema(self):
        self.add_schema({"type": "null"})
        self.assertResult({
            "$schema": SchemaRoot.DEFAULT_URI,
            "type": "null"})

    def test_add_object(self):
        self.add_object(None)
        self.assertResult({
            "$schema": SchemaRoot.DEFAULT_URI,
            "type": "null"})

    def test_to_json(self):
        self.assertEqual(
            self._schema.to_json(),
            '{"$schema": "%s"}' % SchemaRoot.DEFAULT_URI)

    def test_add_schema_with_uri_default(self):
        test_uri = 'TEST_URI'
        self.add_schema({"$schema": test_uri, "type": "null"})
        self.assertResult({"$schema": test_uri, "type": "null"})

    def test_add_schema_with_uri_not_defuult(self):
        test_uri = 'TEST_URI'
        self._schema = SchemaRoot(schema_uri=test_uri)
        self.add_schema({"$schema": 'BAD_URI', "type": "null"})
        self.assertResult({"$schema": test_uri, "type": "null"})
