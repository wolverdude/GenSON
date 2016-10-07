class Tuple:
    PROPERTIES = ('type', 'items')

    def __init__(self):
        self._items = []

    def match_schema(self, schema):
        return schema['type'] == 'array' and isinstance(schema['items'], list)

    def match_object(self, obj):
        return isinstance(obj, list)

    def add_schema(self, schema):
        self._add(schema['items'], 'add_schema')

    def add_object(self, obj):
        self._add(obj, 'add_object')

    def _add(self, items, func):
        while len(self._items) < len(items):
            self._items.append(SchemaNode())

        for subschema, item in zip(self._items, items):
            getattr(subschema, func)(item)

    def to_schema(self):
        return {
            type: 'array',
            items: [item.to_schema() for item in self._items]
        }
