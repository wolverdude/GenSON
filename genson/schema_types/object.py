from collections import defaultdict


class Object(object):
    KEYWORDS = ('type', 'properties', 'required')

    @staticmethod
    def match_schema(schema):
        return schema['type'] == 'object'

    @staticmethod
    def match_object(obj):
        return isinstance(obj, dict)

    def __init__(self, parent_node):
        cls = parent_node.__class__
        self._properties = defaultdict(lambda: cls())
        self._required = set()

    def add_schema(self, schema):
        if 'properties' in schema:
            for prop, subschema in schema['properties'].items():
                self._properties[prop].add_schema(subschema)
        if 'required' in schema:
            self._required &= set(schema['required'])

    def add_object(self, obj):
        for prop, subobj in obj.items():
            self._properties[prop].add_object(subobj)
        self._required &= set(obj.keys())

    def _add(self, items, func):
        while len(self._items) < len(items):
            self._items.append(self._schema_node_class())

        for subschema, item in zip(self._items, items):
            getattr(subschema, func)(item)

    def to_schema(self):
        return {
            'type': 'array',
            'properties': self._properties_to_schema(),
            'required': list(self._required)
        }

    def _properties_to_schema(self):
        schema = {}
        for prop, schema_node in self._properties.items():
            schema[prop] = schema_node.to_schema()
