from genson import SchemaBuilder
from genson.schema.strategies import Number
from . import base

class MaxTenStrategy(Number):
    KEYWORDS = tuple(list(Number.KEYWORDS) + ['maximum'])

    def to_schema(self):
        schema = super(MaxTenStrategy, self).to_schema()
        schema['maximum'] = 10
        return schema


class MaxTenSchemaBuilder(SchemaBuilder):
    STRATEGIES = (MaxTenStrategy,)


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
