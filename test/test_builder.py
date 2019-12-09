from . import base
from genson import SchemaBuilder


class TestParams(base.SchemaBuilderTestCase):

    def test_uri(self):
        test_uri = 'TEST_URI'
        self.builder = SchemaBuilder(schema_uri=test_uri)
        self.assertResult({"$schema": test_uri})

    def test_null_uri(self):
        self.builder = SchemaBuilder(schema_uri=None)
        self.assertResult({})


class TestMethods(base.SchemaBuilderTestCase):

    def test_add_schema(self):
        self.add_schema({"type": "null"})
        self.assertResult({
            "$schema": SchemaBuilder.DEFAULT_URI,
            "type": "null"})

    def test_add_object(self):
        self.add_object(None)
        self.assertResult({
            "$schema": SchemaBuilder.DEFAULT_URI,
            "type": "null"})

    def test_to_json(self):
        self.assertEqual(
            self.builder.to_json(),
            '{"$schema": "%s"}' % SchemaBuilder.DEFAULT_URI)

    def test_add_schema_with_uri_default(self):
        test_uri = 'TEST_URI'
        self.add_schema({"$schema": test_uri, "type": "null"})
        self.assertResult({"$schema": test_uri, "type": "null"})

    def test_add_schema_with_uri_not_defuult(self):
        test_uri = 'TEST_URI'
        self.builder = SchemaBuilder(schema_uri=test_uri)
        self.add_schema({"$schema": 'BAD_URI', "type": "null"})
        self.assertResult({"$schema": test_uri, "type": "null"})

    def test_empty_falsy(self):
        self.assertIs(bool(self.builder), False)

    def test_full_truty(self):
        self.add_object(None)
        self.assertIs(bool(self.builder), True)


class TestInteraction(base.SchemaBuilderTestCase):

    def test_add_other(self):
        test_uri = 'TEST_URI'
        other = SchemaBuilder(schema_uri=test_uri)
        other.add_object(1)
        self.add_object('one')
        self.add_schema(other)
        self.assertResult({
            "$schema": test_uri,
            "type": ["integer", "string"]})

    def test_add_other_no_uri_overwrite(self):
        test_uri = 'TEST_URI'
        other = SchemaBuilder()
        other.add_object(1)
        self.add_object('one')
        self.add_schema(other)
        self.add_schema({'$schema': test_uri})
        self.assertResult({
            "$schema": test_uri,
            "type": ["integer", "string"]})

    def test_eq(self):
        b1 = SchemaBuilder()
        b1.add_object(1)
        b2 = SchemaBuilder()
        b2.add_object(1)
        self.assertEqual(b1, b2)

    def test_ne(self):
        b1 = SchemaBuilder()
        b1.add_object(1)
        b2 = SchemaBuilder()
        b2.add_object('one')
        self.assertNotEqual(b1, b2)
