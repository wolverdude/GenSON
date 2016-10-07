class List:
    PROPERTIES = ('type', 'items')

    def __init__(self):
        self._items = SchemaNode()

    def match_schema(self, schema):
        return schema['type'] == 'array' and isinstance(schema['items'], dict)

    def match_object(self, obj):
        return isinstance(obj, list)

    def add_schema(self, schema):
        self._items.add_schema(schema['items'])

    def add_object(self, obj):
        for item in obj:
            self._items.add_object(item)

    def to_schema(self):
        return {
            type: 'array',
            items: items.to_schema()
        }
