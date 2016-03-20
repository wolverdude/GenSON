import unittest
import base

def check(self, instance, options, expected):  # alias for readability
    return self.assertGenSchema(instance, options, expected)

class TestBasicTypes(base.SchemaTestCase):

    def test_no_object(self):
        s = base.Schema()
        self.assertSchema(s.to_dict(), {})

    def test_string(self):
        check(self, "string", {}, {"type": "string"})

    def test_integer(self):
        check(self, 1, {}, {"type": "integer"})

    def test_number(self):
        check(self, 1.1, {}, {"type": "number"})

    def test_boolean(self):
        check(self, True, {}, {"type": "boolean"})

    def test_null(self):
        check(self, None, {}, {"type": "null"})


class TestArray(base.SchemaTestCase):

    def test_empty(self):
        check(self, [], {}, {"type": "array", "items": {}})

    def test_empty_sep(self):
        check(self, [], {"merge_arrays": False}, {"type": "array"})

    @unittest.expectedFailure
    def test_empty_BAD(self):       # Empty array is not a valid schema
        check(self, [], {}, {"type": "array", "items": []})

    @unittest.expectedFailure
    def test_monotype_BAD(self):    # Items should be dict, not list
        instance = ["spam", "spam", "spam", "egg", "spam"]
        expected = {"type": "array", "items": [{"type": "string"}]}
        check(self, instance, {}, expected)

    def test_monotype(self):
        instance = ["spam", "spam", "spam", "egg", "spam"]
        expected = {"type": "array", "items": {"type": "string"}}
        check(self, instance, {}, expected)

    def test_bitype(self):   # both instances validate against merged array
        instance1 = ["spam", 1, "spam", "egg", "spam"]
        instance2 = [1, "spam", "spam", "egg", "spam"]
        expected = {"type": "array", "items": {"type": ["integer","string"]}}
        actual = check(self, instance1, {}, expected)
        self.assertValidData(instance2, actual)

    def test_bitype_sep(self):   # instance 2 doesn't validate against tuple array
        instance1 = ["spam", 1, "spam", "egg", "spam"]
        instance2 = [1, "spam", "spam", "egg", "spam"]
        expected = {"type": "array",
                    "items": [{"type": "string"},
                              {"type":"integer"},
                              {"type": "string"},
                              {"type": "string"},
                              {"type": "string"}]}
        actual = check(self, instance1, {"merge_arrays": False}, expected)
        self.assertInvalidData(instance2, actual)

    def test_multitype_merge(self):
        instance = [1, "2", None, False]
        expected = {
            "type": "array",
            "items": {
                "type": ["boolean", "integer", "null", "string"]}
        }
        check(self, instance, {}, expected)

    def test_multitype_sep(self):
        instance = [1, "2", "3", None, False]
        expected = {
            "type": "array",
            "items": [
                {"type": "integer"},
                {"type": "string"},
                {"type": "string"},
                {"type": "null"},
                {"type": "boolean"}]
        }
        check(self, instance, {"merge_arrays": False}, expected)

    def test_2deep(self):
        instance = [1, "2", [3.14, 4, "5"], None, False]
        expected = {
            "type": "array",
            "items": [
                {"type": "integer"},
                {"type": "string"},
                {"type": "array",
                "items": [
                    {"type": "number"},
                    {"type": "integer"},
                    {"type": "string"}]},
                {"type": "null"},
                {"type": "boolean"}]
        }
        check(self, instance, {"merge_arrays": False}, expected)


class TestObject(base.SchemaTestCase):

    def test_empty_object(self):
        check(self, {}, {}, {"type": "object", "properties": {}})

    def test_basic_object(self):
        instance = {
            "Red Windsor": "Normally, but today the van broke down.",
            "Stilton": "Sorry.",
            "Gruyere": False}
        expected = {
            "required": ["Gruyere", "Red Windsor", "Stilton"],
            "type": "object",
            "properties": {
                "Red Windsor": {"type": "string"},
                "Gruyere": {"type": "boolean"},
                "Stilton": {"type": "string"}
            }
        }
        check(self, instance, {}, expected)


class TestComplex(base.SchemaTestCase):

    def test_array_reduce(self):
        instance = [
            ["surprise"],
            ["fear", "surprise"],
            ["fear", "surprise", "ruthless efficiency"],
            ["fear", "surprise", "ruthless efficiency",
                  "an almost fanatical devotion to the Pope"]
        ]
        expected = {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "string"}}
        }
        check(self, instance, {}, expected)

    def test_array_in_object(self):
        instance = {"a": "b", "c": [1, 2, 3]}
        expected = {
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
        check(self, instance, {}, expected)

    def test_object_in_array(self):
        instance = [
            {"name": "Sir Lancelot of Camelot",
             "quest": "to seek the Holy Grail",
             "favorite colour": "blue"},
            {"name": "Sir Robin of Camelot",
             "quest": "to seek the Holy Grail",
             "capitol of Assyria": None}]
        expected = {
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
        check(self, instance, {}, expected)

    def test_three_deep(self):
        instance = {"matryoshka": {"design": {"principle": "FTW!"}}}
        expected = {
            "type": "object",
            "required": ["matryoshka"],
            "properties": {
                "matryoshka": {
                    "type": "object",
                    "required": ["design"],
                    "properties": {"design": {
                        "type": "object",
                        "required": ["principle"],
                        "properties": {
                            "principle": {"type": "string"}
                        }
                    }}
                }
            }
        }
        check(self, instance, {}, expected)

if __name__ == "__main__":
    unittest.main()
