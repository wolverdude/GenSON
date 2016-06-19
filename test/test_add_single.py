from . import base


class TestType(base.SchemaTestCase):

    def test_no_schema(self):
        schema = {}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_single_type(self):
        schema = {'type': 'string'}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_single_type_unicode(self):
        schema = {u'type': u'string'}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_multi_type(self):
        schema = {'type': ['boolean', 'null', 'number', 'string']}
        self.add_schema(schema)
        self.assertResult(schema)


class TestPreserveKeys(base.SchemaTestCase):

    def test_preserves_existing_keys(self):
        schema = {'type': 'number', 'value': 5}
        self.add_schema(schema)
        self.assertResult(schema)
