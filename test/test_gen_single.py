import unittest
import base


class TestBasicTypes(base.SchemaTestCase):

    def test_no_object(self):
        s = base.Schema()
        self.assertSchema(s.to_dict(), {})

    def test_string(self):
        self.assertGenSchema("string", {}, {"type": "string"})

    def test_integer(self):
        self.assertGenSchema(1, {}, {"type": "integer"})

    def test_number(self):
        self.assertGenSchema(1.1, {}, {"type": "number"})

    def test_boolean(self):
        self.assertGenSchema(True, {}, {"type": "boolean"})

    def test_null(self):
        self.assertGenSchema(None, {}, {"type": "null"})


class TestArray(base.SchemaTestCase):

    def test_empty(self):
        self.assertGenSchema([], {}, {"type": "array", "items": {}})

    def test_empty_sep(self):
        self.assertGenSchema([], {"merge_arrays": False}, {"type": "array"})

    def test_monotype(self):
        instance = ["spam", "spam", "spam", "egg", "spam"]
        expected = {"type": "array", "items": {"type": "string"}}
        self.assertGenSchema(instance, {}, expected)

    def test_bitype(self):   # both instances validate against merged array
        instance1 = ["spam", 1, "spam", "egg", "spam"]
        instance2 = [1, "spam", "spam", "egg", "spam"]
        expected = {"type": "array", "items": {"type": ["integer","string"]}}
        actual = self.assertGenSchema(instance1, {}, expected)
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
        actual = self.assertGenSchema(instance1, {"merge_arrays": False}, expected)
        self.assertInvalidData(instance2, actual)

    def test_multitype_merge(self):
        instance = [1, "2", None, False]
        expected = {
            "type": "array",
            "items": {
                "type": ["boolean", "integer", "null", "string"]}
        }
        self.assertGenSchema(instance, {}, expected)

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
        self.assertGenSchema(instance, {"merge_arrays": False}, expected)

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
        self.assertGenSchema(instance, {"merge_arrays": False}, expected)


class TestObject(base.SchemaTestCase):

    def test_empty_object(self):
        self.assertGenSchema({}, {}, {"type": "object", "properties": {}})

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
        self.assertGenSchema(instance, {}, expected)


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
        self.assertGenSchema(instance, {}, expected)

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
        self.assertGenSchema(instance, {}, expected)

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
        self.assertGenSchema(instance, {}, expected)

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
        self.assertGenSchema(instance, {}, expected)

if __name__ == "__main__":
    unittest.main()
