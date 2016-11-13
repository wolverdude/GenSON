class Tuple:
    KEYWORDS = ('type', 'items')

    @staticmethod
    def match_schema(schema):
        return schema['type'] == 'array' and isinstance(schema['items'], list)

    @staticmethod
    def match_object(obj):
        return isinstance(obj, list)

    def __init__(self, parent_node):
        self._schema_node_class = parent_node.__class__
        self._items = []

    def add_schema(self, schema):
        self._add(schema['items'], 'add_schema')

    def add_object(self, obj):
        self._add(obj, 'add_object')

    def _add(self, items, func):
        while len(self._items) < len(items):
            self._items.append(self._schema_node_class())

        for subschema, item in zip(self._items, items):
            getattr(subschema, func)(item)

    def to_schema(self):
        schema = {'type': 'array'}
        if self._items:
            schema['items'] = [item.to_schema() for item in self._items]
        return schema
