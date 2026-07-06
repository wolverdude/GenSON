import unittest
from genson import SchemaBuilder
from genson.schema.strategies import (
    SchemaStrategy, Number, BASIC_SCHEMA_STRATEGIES)
from . import base


class MaxTenStrategy(Number):
    KEYWORDS = tuple(list(Number.KEYWORDS) + ['maximum'])

    def to_schema(self):
        schema = super().to_schema()
        schema['maximum'] = 10
        return schema


class FalseStrategy(SchemaStrategy):
    KEYWORDS = tuple(list(SchemaStrategy.KEYWORDS) + ['const'])

    @classmethod
    def match_schema(self, schema):
        return True

    @classmethod
    def match_object(self, obj):
        return True

    def to_schema(self):
        schema = super().to_schema()
        schema['type'] = 'boolean'
        schema['const'] = False
        return schema


class MaxTenSchemaBuilder(SchemaBuilder):
    EXTRA_STRATEGIES = (MaxTenStrategy,)


class FalseSchemaBuilder(SchemaBuilder):
    STRATEGIES = (FalseStrategy,)


class TestExtraStrategies(base.SchemaNodeTestCase):
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


class DuplicateStrategiesSchemaBuilder(SchemaBuilder):
    """many duplicate strategies to exercise deduplication"""
    EXTRA_STRATEGIES = BASIC_SCHEMA_STRATEGIES * 100


class TestStrategyDeduplication(unittest.TestCase):

    def test_deduplicates_strategies(self):
        strategies = DuplicateStrategiesSchemaBuilder.STRATEGIES
        self.assertEqual(len(strategies), len(set(strategies)))

    def test_preserves_first_occurrence_order(self):
        self.assertEqual(DuplicateStrategiesSchemaBuilder.STRATEGIES,
                         tuple(BASIC_SCHEMA_STRATEGIES))

    def test_extra_strategies_keep_priority(self):
        # EXTRA_STRATEGIES stay ahead of the inherited strategies even
        # when they duplicate each other
        class DupExtra(SchemaBuilder):
            EXTRA_STRATEGIES = (MaxTenStrategy, MaxTenStrategy)

        self.assertIs(DupExtra.STRATEGIES[0], MaxTenStrategy)
        self.assertEqual(DupExtra.STRATEGIES.count(MaxTenStrategy), 1)


class TestClobberStrategies(base.SchemaNodeTestCase):
    CLASS = FalseSchemaBuilder

    def test_add_object(self):
        self.add_object("Any Norwegian Jarlsberger?")
        self.assertResult({
            '$schema': 'http://json-schema.org/schema#',
            'type': 'boolean',
            'const': False}, enforceUserContract=False)

    def test_add_schema(self):
        self.add_schema({'type': 'string'})
        self.assertResult({
            '$schema': 'http://json-schema.org/schema#',
            'type': 'boolean',
            'const': False}, enforceUserContract=False)
