from unittest.mock import MagicMock
from . import base
from genson import SchemaRoot


class TestParams(base.SchemaRootTestCase):

    def test_node_class(self):
        mock_node = MagicMock()
        mock_node.to_schema.return_value = {"type": "null"}
        self._schema = SchemaRoot(node_class=lambda: mock_node)
        self.assertResult({
            "$schema": SchemaRoot.DEFAULT_URL,
            "type": "null"})

    def test_url(self):
        test_url = 'TEST_URL'
        self._schema = SchemaRoot(url=test_url)
        self.assertResult({"$schema": test_url})


class TestMethods(base.SchemaRootTestCase):

    def test_add_schema(self):
        self.add_schema({"type": "null"})
        self.assertResult({
            "$schema": SchemaRoot.DEFAULT_URL,
            "type": "null"})

    def test_add_object(self):
        self.add_object(None)
        self.assertResult({
            "$schema": SchemaRoot.DEFAULT_URL,
            "type": "null"})

    def test_to_json(self):
        self.assertEqual(
            self._schema.to_schema(),
            '{"$schema":"%s"}' % SchemaRoot.DEFAULT_URL)
