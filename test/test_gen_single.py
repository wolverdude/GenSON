import unittest
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from genson import Schema


class TestBasicTypes(unittest.TestCase):

    def test_no_object(self):
        s = Schema()
        self.assertEqual(s.to_dict(), {})

    def test_string(self):
        s = Schema().add_object("string")
        self.assertEqual(s.to_dict(), {"type": "string"})

    def test_integer(self):
        s = Schema().add_object(1)
        self.assertEqual(s.to_dict(), {"type": "integer"})

    def test_number(self):
        s = Schema().add_object(1.1)
        self.assertEqual(s.to_dict(), {"type": "number"})

    def test_boolean(self):
        s = Schema().add_object(True)
        self.assertEqual(s.to_dict(), {"type": "boolean"})

    def test_null(self):
        s = Schema().add_object(None)
        self.assertEqual(s.to_dict(), {"type": "null"})


class TestArray(unittest.TestCase):

    def test_empty(self):
        s = Schema().add_object([])
        self.assertEqual(s.to_dict(),
                         {"type": "array", "items": []})

    def test_monotype(self):
        s = Schema().add_object(["spam", "spam", "spam", "egg", "spam"])
        self.assertEqual(s.to_dict(),
                         {"type": "array", "items": [{"type": "string"}]})

    def test_multitype_merge(self):
        s = Schema().add_object([1, "2", None, False])
        self.assertEqual(s.to_dict(), {
            "type": "array",
            "items": [{
                "type": ["boolean", "integer", "null", "string"]}]
            })

    def test_multitype_sep(self):
        s = Schema(merge_arrays=False).add_object([1, "2", None, False])
        self.assertEqual(s.to_dict(), {
            "type": "array",
            "items": [
                {"type": "integer"},
                {"type": "string"},
                {"type": "null"},
                {"type": "boolean"}]
            })


class TestObject(unittest.TestCase):

    def test_empty_object(self):
        s = Schema().add_object({})
        self.assertEqual(s.to_dict(), {"type": "object", "properties": {}})

    def test_basic_object(self):
        s = Schema().add_object({
            "Red Windsor": "Normally, but today the van broke down.",
            "Stilton": "Sorry.",
            "Gruyere": False})
        self.assertEqual(s.to_dict(), {
            "required": ["Gruyere", "Red Windsor", "Stilton"],
            "type": "object",
            "properties": {
                "Red Windsor": {"type": "string"},
                "Gruyere": {"type": "boolean"},
                "Stilton": {"type": "string"}}
            })


class TestComplex(unittest.TestCase):

    def test_array_reduce(self):
        s = Schema().add_object([["surprise"],
                                 ["fear", "surprise"],
                                 ["fear", "surprise", "ruthless efficiency"],
                                 ["fear", "surprise", "ruthless efficiency",
                                  "an almost fanatical devotion to the Pope"]])
        self.assertEqual(s.to_dict(), {
            "type": "array",
            "items": [{
                "type": "array",
                "items": [{"type": "string"}]}]
            })

    def test_array_in_object(self):
        s = Schema().add_object({"a": "b", "c": [1, 2, 3]})
        self.assertEqual(s.to_dict(), {
            "required": [
                "a",
                "c"
            ],
            "type": "object",
            "properties": {
                "a": {
                    "type": "string"
                },
                "c": {
                    "items": [
                        {
                            "type": "integer"
                        }
                    ],
                    "type": "array"
                }
            }
        })

    def test_object_in_array(self):
        s = Schema().add_object([
            {"name": "Sir Lancelot of Camelot",
             "quest": "to seek the Holy Grail",
             "favorite colour": "blue"},
            {"name": "Sir Robin of Camelot",
             "quest": "to seek the Holy Grail",
             "capitol of Assyria": None}])
        self.assertEqual(s.to_dict(), {
            "items": [
                {
                    "required": [
                        "name",
                        "quest"
                    ],
                    "type": "object",
                    "properties": {
                        "quest": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "favorite colour": {
                            "type": "string"
                        },
                        "capitol of Assyria": {
                            "type": "null"
                        }
                    }
                }
            ],
            "type": "array"
        })

    def test_three_deep(self):
        s = Schema().add_object(
            {"matryoshka": {"design": {"principle": "FTW!"}}})
        self.assertEqual(s.to_dict(), {
            "required": ["matryoshka"],
            "type": "object",
            "properties": {"matryoshka": {
                "required": ["design"],
                "type": "object",
                "properties": {"design": {
                    "required": ["principle"],
                    "type": "object",
                    "properties": {"principle": {"type": "string"}}}}
                }}
            })


if __name__ == "__main__":
    unittest.main()
