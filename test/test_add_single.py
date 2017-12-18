import warnings
from . import base


class TestType(base.SchemaTestCase):

    def test_single_type(self):
        schema = {'type': 'string'}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_single_type_unicode(self):
        schema = {u'type': u'string'}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_no_type(self):
        schema = {'title': 'ambiguous schema'}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.add_schema(schema)
        self.assertResult(schema)


class TestAnyOf(base.SchemaTestCase):

    def test_multi_type(self):
        schema = {'type': ['boolean', 'null', 'number', 'string']}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_anyof(self):
        schema = {"anyOf": [
            {"type": "null"},
            {"type": "boolean", "title": "Gruyere"}
        ]}
        self.add_schema(schema)
        self.assertResult(schema)


class TestPreserveKeys(base.SchemaTestCase):

    def test_preserves_existing_keys(self):
        schema = {'type': 'number', 'const': 5, 'my-custom-key': True}
        self.add_schema(schema)
        self.assertResult(schema)
