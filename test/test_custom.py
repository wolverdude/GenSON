import unittest
from genson import SchemaBuilder
from genson.schema.strategies import (
    SchemaStrategy, Number, List, Tuple, Object, BASIC_SCHEMA_STRATEGIES)
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


class RecordingMixin(SchemaStrategy):
    """
    cooperative-inheritance mixin that records every object routed to a
    strategy. It relies on each concrete strategy's ``add_object``
    override chaining up through ``super().add_object`` -- exactly the
    contract PR #79 restored for ``Number``.
    """
    # each concrete subclass supplies its own list
    log = None

    def add_object(self, obj):
        type(self).log.append(obj)
        super().add_object(obj)


class RecordingNumber(Number, RecordingMixin):
    log = []


class RecordingList(List, RecordingMixin):
    log = []


class RecordingTuple(Tuple, RecordingMixin):
    log = []


class RecordingObject(Object, RecordingMixin):
    log = []


class RecordingNumberBuilder(SchemaBuilder):
    STRATEGIES = (RecordingNumber,)


class RecordingListBuilder(SchemaBuilder):
    STRATEGIES = (RecordingList,)


class RecordingTupleBuilder(SchemaBuilder):
    STRATEGIES = (RecordingTuple,)


class RecordingObjectBuilder(SchemaBuilder):
    STRATEGIES = (RecordingObject,)


class TestAddObjectSuperChaining(unittest.TestCase):
    """
    Every built-in strategy that overrides ``add_object`` must call
    ``super().add_object`` so cooperative subclass hooks run. PR #79
    fixed this for ``Number``; ``List``, ``Tuple`` and ``Object`` must
    honour the same contract.
    """

    def setUp(self):
        for cls in (RecordingNumber, RecordingList,
                    RecordingTuple, RecordingObject):
            cls.log = []

    def test_number_super_chaining(self):
        # control: already fixed by PR #79
        RecordingNumberBuilder().add_object(5)
        self.assertEqual(RecordingNumber.log, [5])

    def test_list_super_chaining(self):
        # empty container isolates the hook from item recursion
        RecordingListBuilder().add_object([])
        self.assertEqual(RecordingList.log, [[]])

    def test_tuple_super_chaining(self):
        RecordingTupleBuilder().add_object([])
        self.assertEqual(RecordingTuple.log, [[]])

    def test_object_super_chaining(self):
        RecordingObjectBuilder().add_object({})
        self.assertEqual(RecordingObject.log, [{}])

    def test_nested_object_and_array_hooks_all_fire(self):
        # a single nested value must reach the hook at every level:
        # outer object -> inner list -> inner objects
        class NestedBuilder(SchemaBuilder):
            STRATEGIES = (RecordingObject, RecordingList, RecordingNumber)

        NestedBuilder().add_object({'items': [{'n': 1}, {'n': 2}]})
        self.assertEqual(RecordingObject.log,
                         [{'items': [{'n': 1}, {'n': 2}]},
                          {'n': 1}, {'n': 2}])
        self.assertEqual(RecordingList.log, [[{'n': 1}, {'n': 2}]])
        self.assertEqual(RecordingNumber.log, [1, 2])


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
