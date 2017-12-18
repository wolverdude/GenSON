from builtins import super
from .base import SchemaGenerator


class List(SchemaGenerator):
    KEYWORDS = ('type', 'items')

    @staticmethod
    def match_schema(schema):
        return schema.get('type') == 'array' and isinstance(schema['items'], dict)

    @staticmethod
    def match_object(obj):
        return isinstance(obj, list)

    def __init__(self, parent_node):
        super().__init__(parent_node)
        self._items = parent_node.__class__()

    def add_schema(self, schema):
        super().add_schema(schema)
        self._items.add_schema(schema['items'])

    def add_object(self, obj):
        for item in obj:
            self._items.add_object(item)

    def to_schema(self):
        schema = super().to_schema()
        schema['type'] = 'array'
        schema['items'] = self._items.to_schema()
        return schema


class Tuple(SchemaGenerator):
    KEYWORDS = ('type', 'items')

    @staticmethod
    def match_schema(schema):
        return schema.get('type') == 'array' and isinstance(schema['items'], list)

    @staticmethod
    def match_object(obj):
        return isinstance(obj, list)

    def __init__(self, parent_node):
        super().__init__(parent_node)
        self._schema_node_class = parent_node.__class__
        self._items = []

    def add_schema(self, schema):
        super().add_schema(schema)
        self._add(schema['items'], 'add_schema')

    def add_object(self, obj):
        self._add(obj, 'add_object')

    def _add(self, items, func):
        while len(self._items) < len(items):
            self._items.append(self._schema_node_class())

        for subschema, item in zip(self._items, items):
            getattr(subschema, func)(item)

    def to_schema(self):
        schema = super().to_schema()
        schema['type'] = 'array'
        if self._items:
            schema['items'] = [item.to_schema() for item in self._items]
        return schema
