class List:
    KEYWORDS = ('type', 'items')

    @staticmethod
    def match_schema(schema):
        return schema['type'] == 'array' and isinstance(schema['items'], dict)

    @staticmethod
    def match_object(obj):
        return isinstance(obj, list)

    def __init__(self, parent_node):
        self._items = parent_node.__class__()

    def add_schema(self, schema):
        self._items.add_schema(schema['items'])

    def add_object(self, obj):
        for item in obj:
            self._items.add_object(item)

    def to_schema(self):
        return {
            'type': 'array',
            'items': self._items.to_schema()
        }
