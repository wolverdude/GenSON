from genson import custom_schema_builder
from genson.schema.generators import Number
from . import base

class MaxTenGenerator(Number):
    KEYWORDS = tuple(list(Number.KEYWORDS) + ['maximum'])

    def to_schema(self):
        schema = super(MaxTenGenerator, self).to_schema()
        schema['maximum'] = 10
        return schema


MaxTenSchemaBuilder = custom_schema_builder([MaxTenGenerator])


class TestBasicTypes(base.SchemaNodeTestCase):
    CLASS = MaxTenSchemaBuilder

    def test_add_object(self):
        self.add_object(5)
        self.assertResult({
            '$schema': 'http://json-schema.org/schema#',
            'type': 'integer',
            'maximum': 10})

    def test_add_schema(self):
        self.add_schema({'type': 'integer'})
        self.assertResult({
            '$schema': 'http://json-schema.org/schema#',
            'type': 'integer',
            'maximum': 10})
