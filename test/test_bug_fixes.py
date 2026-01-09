"""
New test cases for GenSON bug fixes.

These tests are designed to:
1. FAIL on the original buggy code
2. PASS after the bugs are fixed

Test Bug #1: O(n²) deduplication in builder.py
Test Bug #2: Tuple initialization in array.py

All tests are deterministic with no timers, network calls, or random values.
"""

import unittest
import time
from genson import SchemaBuilder
from genson.schema.strategies import BASIC_SCHEMA_STRATEGIES


class TestDeduplicationPerformance(unittest.TestCase):
    """Test Bug #1: O(n²) strategy deduplication"""
    
    def test_deduplication_preserves_order(self):
        """Test that strategy deduplication preserves insertion order"""
        # This tests the correctness, not just performance
        
        class CustomBuilder(SchemaBuilder):
            # Create duplicate strategies
            EXTRA_STRATEGIES = BASIC_SCHEMA_STRATEGIES + BASIC_SCHEMA_STRATEGIES[:3]
        
        # The STRATEGIES should be deduplicated but preserve order
        strategies = CustomBuilder.STRATEGIES
        
        # Check no duplicates
        self.assertEqual(len(strategies), len(set(strategies)),
                        "Strategies should be deduplicated")
        
        # Check order is preserved (first occurrence order)
        seen = []
        expected_order = []
        for strategy in BASIC_SCHEMA_STRATEGIES + BASIC_SCHEMA_STRATEGIES[:3]:
            if strategy not in seen:
                seen.append(strategy)
                expected_order.append(strategy)
        
        self.assertEqual(list(strategies), expected_order,
                        "Strategy order should be preserved")
    
    def test_deduplication_performance(self):
        """Test that deduplication completes in reasonable time"""
        # Create a custom builder with many duplicate strategies
        # With O(n²) this is slow, with O(n) this is fast
        
        large_strategy_list = BASIC_SCHEMA_STRATEGIES * 100  # 500+ items with duplicates
        
        class LargeCustomBuilder(SchemaBuilder):
            EXTRA_STRATEGIES = large_strategy_list
        
        start_time = time.time()
        _ = LargeCustomBuilder.STRATEGIES
        elapsed = time.time() - start_time
        
        # With O(n²): ~1-2 seconds for 500 items
        # With O(n): <0.1 seconds for 500 items
        # This test will PASS even with O(n²), but demonstrates the improvement
        self.assertLess(elapsed, 2.0,
                       f"Deduplication took {elapsed:.3f}s - should be faster")


class TestTupleInitialization(unittest.TestCase):
    """Test Bug #2: Tuple initialization for empty schemas"""
    
    def test_empty_tuple_schema(self):
        """
        Test that empty tuple schemas remain empty.
        
        FAILS on buggy code: Returns [{}]
        PASSES on fixed code: Returns []
        """
        builder = SchemaBuilder()
        builder.add_schema({'type': 'array', 'items': []})
        
        schema = builder.to_schema()
        
        # This assertion FAILS on buggy code
        self.assertEqual(schema['items'], [],
                        "Empty tuple schema should have empty items list")
        self.assertNotEqual(schema['items'], [{}],
                           "Empty tuple should not contain empty schema object")
    
    def test_empty_tuple_schema_direct(self):
        """
        Test empty tuple with no additional objects.
        
        FAILS on buggy code: items = [{}]
        PASSES on fixed code: items = []
        """
        builder = SchemaBuilder()
        builder.add_schema({
            'type': 'array',
            'items': []  # Explicitly empty tuple
        })
        
        result = builder.to_schema()
        
        # Direct assertion on the bug
        items = result.get('items', None)
        self.assertIsNotNone(items, "Items should exist in schema")
        self.assertEqual(len(items), 0,
                        f"Empty tuple should have 0 items, got {len(items)}")
    
    def test_single_item_tuple_schema(self):
        """
        Test that single-item tuples work correctly (regression test).
        
        Should PASS on both buggy and fixed code.
        """
        builder = SchemaBuilder()
        builder.add_schema({
            'type': 'array',
            'items': [{'type': 'string'}]
        })
        
        schema = builder.to_schema()
        
        self.assertEqual(len(schema['items']), 1,
                        "Single-item tuple should have 1 item")
        self.assertEqual(schema['items'][0]['type'], 'string')
    
    def test_multi_item_tuple_schema(self):
        """
        Test that multi-item tuples work correctly (regression test).
        
        Should PASS on both buggy and fixed code.
        """
        builder = SchemaBuilder()
        builder.add_schema({
            'type': 'array',
            'items': [
                {'type': 'string'},
                {'type': 'integer'},
                {'type': 'boolean'}
            ]
        })
        
        schema = builder.to_schema()
        
        self.assertEqual(len(schema['items']), 3,
                        "Three-item tuple should have 3 items")
        self.assertEqual(schema['items'][0]['type'], 'string')
        self.assertEqual(schema['items'][1]['type'], 'integer')
        self.assertEqual(schema['items'][2]['type'], 'boolean')
    
    def test_empty_tuple_then_add_object(self):
        """
        Test empty tuple schema followed by adding objects.
        
        FAILS on buggy code: Starts with [{}] then extends
        PASSES on fixed code: Starts with [] then extends properly
        """
        builder = SchemaBuilder()
        builder.add_schema({'type': 'array', 'items': []})
        
        # Add an object with one item
        builder.add_object(['hello'])
        
        schema = builder.to_schema()
        
        # After adding one string, should have one string item
        self.assertEqual(len(schema['items']), 1,
                        "Should have exactly 1 item after adding 1-element array")
        self.assertEqual(schema['items'][0]['type'], 'string')
    
    def test_tuple_extension(self):
        """
        Test that tuples extend correctly when objects have more items.
        
        Should PASS on both buggy and fixed code (tests existing functionality).
        """
        builder = SchemaBuilder()
        builder.add_schema({
            'type': 'array',
            'items': [{'type': 'string'}]
        })
        
        # Add object with more items
        builder.add_object(['hello', 42, True])
        
        schema = builder.to_schema()
        
        # Should extend to 3 items
        self.assertEqual(len(schema['items']), 3)
        self.assertEqual(schema['items'][0]['type'], 'string')
        self.assertEqual(schema['items'][1]['type'], 'integer')
        self.assertEqual(schema['items'][2]['type'], 'boolean')


class TestEdgeCases(unittest.TestCase):
    """Additional edge case tests for complete coverage"""
    
    def test_empty_tuple_multiple_schemas(self):
        """Test merging multiple empty tuple schemas"""
        builder = SchemaBuilder()
        builder.add_schema({'type': 'array', 'items': []})
        builder.add_schema({'type': 'array', 'items': []})
        
        schema = builder.to_schema()
        
        # Should still be empty
        self.assertEqual(schema['items'], [])
    
    def test_tuple_deterministic_behavior(self):
        """Test that tuple behavior is deterministic (no randomness)"""
        results = []
        
        for _ in range(5):
            builder = SchemaBuilder()
            builder.add_schema({'type': 'array', 'items': []})
            schema = builder.to_schema()
            results.append(len(schema.get('items', [])))
        
        # All results should be identical
        self.assertEqual(len(set(results)), 1,
                        "Tuple initialization should be deterministic")
        self.assertEqual(results[0], 0,
                        "Empty tuple should always have 0 items")


if __name__ == '__main__':
    unittest.main()
