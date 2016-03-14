import unittest
import os
import sys
import jsonschema
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from genson import Schema

def check(c, s, instance, answer):
    schema = s.to_dict()
    c.assertEqual(schema, answer)
    try:
        jsonschema.validate(instance, schema)
    except jsonschema.ValidationError:
        print('ValidationError')

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

    def test_empty_merge(self):
        instance = []
        answer = {"type": "array", "items": {}}
        schema = Schema().add_object(instance)
        check(self, schema, instance, answer)

    def test_empty_sep(self):
        instance = []
        answer = {"type": "array"}
        schema = Schema(merge_arrays=False).add_object(instance)
        check(self, schema, instance, answer)

#    def test_empty_BAD(self):   # empty list is not a valid schema
#        instance = []
#        answer = {"type": "array", "items": []}
#        schema = Schema().add_object(instance)
#        check(self, schema, instance, answer)

    def test_monotype(self):
        instance = ["spam", "spam", "spam", "egg", "spam"]
        answer = {"type": "array", "items": {"type": "string"}}
        schema = Schema().add_object(instance)
        check(self, schema, instance, answer)

    def test_bitype1(self):
        instance = ["spam", 1, "spam", "egg", "spam"]
        answer = {"type": "array", "items": {"type": ["integer","string"]}}
        schema = Schema().add_object(instance)
        check(self, schema, instance, answer)

    def test_bitype2(self):         # succeeds if instance 2 is checked
        instance1 = ["spam", 1, "spam", "egg", "spam"]
        instance2 = [1, "spam", "spam", "egg", "spam"]
        answer = {"type": "array", "items": {"type": ["integer","string"]}}
        schema = Schema().add_object(instance1)
        check(self, schema, instance2, answer)

    def test_bitype2_sep(self):     # ValidationError if instance 2 is checked
        instance1 = ["spam", 1]
        instance2 = [1, "spam"]
        answer = {"type": "array", "items": [{"type": "string"},{"type":"integer"}]}
        schema = Schema(merge_arrays=False).add_object(instance1)
        check(self, schema, instance2, answer)

    def test_multitype_merge(self):
        instance = [1, "2", None, False]
        answer = {
            "type": "array",
            "items": {
                "type": ["boolean", "integer", "null", "string"]}
            }
        schema = Schema().add_object(instance)
        check(self, schema, instance, answer)

    def test_multitype_sep1(self):
        instance = [1, "2", None, False]
        answer = {
            "type": "array",
            "items": [
                {"type": "integer"},
                {"type": "string"},
                {"type": "null"},
                {"type": "boolean"}]
            }
        schema = Schema(merge_arrays=False).add_object(instance)
        check(self, schema, instance, answer)

    def test_multitype_sep2(self):
        instance = [1, "2", "3", None, False]
        answer = {
            "type": "array",
            "items": [
                {"type": "integer"},
                {"type": "string"},
                {"type": "string"},
                {"type": "null"},
                {"type": "boolean"}]
            }
        schema = Schema(merge_arrays=False).add_object(instance)
        check(self, schema, instance, answer)

    def test_2deep_sep(self):
        instance = [1, "2", [3.14, "4"], None, False]
        answer = {
            "type": "array",
            "items": [
                {"type": "integer"},
                {"type": "string"},
                {"type": "array",
                "items": [
                    {"type": "number"},
                    {"type": "string"}]},
                {"type": "null"},
                {"type": "boolean"}]
            }
        schema = Schema(merge_arrays=False).add_object(instance)
        check(self, schema, instance, answer)


class TestObject(unittest.TestCase):

    def test_empty_object(self):
        instance = {}
        answer = {"type": "object", "properties": {}}
        schema = Schema().add_object(instance)
        check(self, schema, instance, answer)

    def test_basic_object(self):
        instance = {
            "Red Windsor": "Normally, but today the van broke down.",
            "Stilton": "Sorry.",
            "Gruyere": False}
        answer = {
            "required": ["Gruyere", "Red Windsor", "Stilton"],
            "type": "object",
            "properties": {
                "Red Windsor": {"type": "string"},
                "Gruyere": {"type": "boolean"},
                "Stilton": {"type": "string"}}
            }
        schema = Schema().add_object(instance)
        check(self, schema, instance, answer)


class TestComplex(unittest.TestCase):

    def test_array_reduce(self):
        instance = [["surprise"],
                        ["fear", "surprise"],
                        ["fear", "surprise", "ruthless efficiency"],
                        ["fear", "surprise", "ruthless efficiency",
                        "an almost fanatical devotion to the Pope"]]
        answer = {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "string"}}
            }
        schema = Schema().add_object(instance)
        check(self, schema, instance, answer)

    def test_array_in_object(self):
        instance = {"a": "b", "c": [1, 2, 3]}
        answer = {
            "required": ["a","c"],
            "type": "object",
            "properties": {
                "a": {"type": "string"},
                "c": {
                    "type": "array",
                    "items": {"type": "integer"}
                }
            }
        }
        schema = Schema().add_object(instance)
        check(self, schema, instance, answer)

    def test_object_in_array(self):
        instance = [
            {"name": "Sir Lancelot of Camelot",
             "quest": "to seek the Holy Grail",
             "favorite colour": "blue"},
            {"name": "Sir Robin of Camelot",
             "quest": "to seek the Holy Grail",
             "capitol of Assyria": None}]
        answer = {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name","quest"],
                "properties": {
                    "quest": {"type": "string"},
                    "name": {"type": "string"},
                    "favorite colour": {"type": "string"},
                    "capitol of Assyria": {"type": "null"}
                }
            }
        }
        schema = Schema().add_object(instance)
        check(self, schema, instance, answer)

    def test_three_deep(self):
        instance = {"matryoshka": {"design": {"principle": "FTW!"}}}
        answer = {
            "required": ["matryoshka"],
            "type": "object",
            "properties": {
                "matryoshka": {
                    "required": ["design"],
                    "type": "object",
                    "properties": {
                        "design": {
                            "required": ["principle"],
                            "type": "object",
                            "properties": {"principle": {"type": "string"}}
                        }
                    }
                }
            }
        }
        schema = Schema().add_object(instance)
        check(self, schema, instance, answer)


class TestAdditional(unittest.TestCase):

    def test_additional_items_sep(self):
        instance1 = ["parrot", "dead"]
        instance2 = ["parrot", "dead", "resting"]
        answer = {
            "type": "array",
            "items": [
                {"type":"string"},
                {"type":"string"}],
            "additionalItems": False
        }
        schema = Schema(merge_arrays=False, additional_items=False).add_object(instance1)
        check(self, schema, instance1, answer)    # instance2 fails validation

    def test_additional_items_merge(self):
        instance1 = ["parrot", "dead"]
        instance2 = ["parrot", "dead", "resting"]
        answer = {
            "type": "array",
            "items": {"type":"string"}
        }
        schema = Schema(merge_arrays=True, additional_items=False).add_object(instance1)
        check(self, schema, instance1, answer)    # additionalItems not used
        check(self, schema, instance2, answer)    # both pass

    def test_additional_props(self):
        instance1 = {
            "type": "witch",
            "floats": {
                "wood": True,
                "stone": False
            }}
        instance2 = {
            "type": "witch",
            "floats": {
                "wood": True,
                "stone": False,
                "duck": True
            }}
        answer = {
            'type': 'object',
            'required': ['floats', 'type'],
            'additionalProperties': False,
            'properties': {
                'type': {'type': 'string'},
                'floats': {
                    'type': 'object',
                    'required': ['stone', 'wood'],
                    'additionalProperties': False,
                    'properties': {
                        'wood': {'type': 'boolean'},
                        'stone': {'type': 'boolean'}
                     }
                }
            }
        }
        schema = Schema(additional_props=False).add_object(instance1)
        check(self, schema, instance1, answer)      # instance 2 fails validation


if __name__ == "__main__":
    unittest.main()
