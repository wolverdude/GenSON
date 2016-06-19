from . import base


class TestBasicTypes(base.SchemaTestCase):

    def test_single_type(self):
        self.add_object('bacon')
        self.add_object('egg')
        self.add_object('spam')
        self.assertResult({'type': 'string'})

    def test_multi_type(self):
        self.add_object('string')
        self.add_object(1.1)
        self.add_object(True)
        self.add_object(None)
        self.assertResult({'type': ['boolean', 'null', 'number', 'string']})

    def test_redundant_integer_type(self):
        self.add_object(1)
        self.add_object(1.1)
        self.assertResult({'type': 'number'})


class TestArrayMerge(base.SchemaTestCase):

    def setUp(self):
        base.SchemaTestCase.setUp(self)
        self.set_schema_options(merge_arrays=True)

    def test_empty(self):
        self.add_object([])
        self.add_object([])

        self.assertResult({"type": "array", "items": {}})

    def test_monotype(self):
        self.add_object(["spam", "spam", "spam", "eggs", "spam"])
        self.add_object(["spam", "bacon", "eggs", "spam"])

        self.assertResult({"type": "array", "items": {"type": "string"}})

    def test_multitype(self):
        self.add_object([1, "2", "3", None, False])
        self.add_object([1, 2, "3", False])

        self.assertObjectValidates([1, "2", 3, None, False])
        self.assertResult({
            "type": "array",
            "items": {
                "type": ["boolean", "integer", "null", "string"]}
        })

    def test_nested(self):
        self.add_object([
            ["surprise"],
            ["fear", "surprise"]
        ])
        self.add_object([
            ["fear", "surprise", "ruthless efficiency"],
            ["fear", "surprise", "ruthless efficiency",
             "an almost fanatical devotion to the Pope"]
        ])
        self.assertResult({
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "string"}}
        })


class TestArrayPositional(base.SchemaTestCase):

    def setUp(self):
        base.SchemaTestCase.setUp(self)
        self.set_schema_options(merge_arrays=False)

    def test_empty(self):
        self.add_object([])
        self.assertResult({"type": "array"})

    def test_multitype(self):
        self.add_object([1, "2", "3", None, False])
        self.add_object([1, 2, "3", False])

        self.assertObjectDoesNotValidate([1, "2", 3, None, False])
        self.assertResult({
            "type": "array",
            "items": [
                {"type": "integer"},
                {"type": ["integer", "string"]},
                {"type": "string"},
                {"type": ["boolean", "null"]},
                {"type": "boolean"}]
        })

    def test_nested(self):
        self.add_object([
            ["surprise"],
            ["fear", "surprise"]
        ])
        self.add_object([
            ["fear", "surprise", "ruthless efficiency"],
            ["fear", "surprise", "ruthless efficiency",
             "an almost fanatical devotion to the Pope"]
        ])

        self.assertResult({
            "type": "array",
            "items": [
                {
                    "type": "array",
                    "items": [
                        {"type": "string"},
                        {"type": "string"},
                        {"type": "string"}
                    ]
                },
                {
                    "type": "array",
                    "items": [
                        {"type": "string"},
                        {"type": "string"},
                        {"type": "string"},
                        {"type": "string"}
                    ]
                },
            ]
        })
