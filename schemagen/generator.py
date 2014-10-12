import types
import json
from copy import copy
from collections import defaultdict

JS_TYPES = {
    types.DictType: 'object',
    types.ListType: 'array',
    types.StringType: 'string',
    types.UnicodeType: 'string',
    types.IntType: 'number',
    types.FloatType: 'number',
    types.BooleanType: 'boolean',
    types.NoneType: 'null',
}


class SchemaGen(object):

    def __init__(self, schema=None):
        self._schema = {}
        if schema:
            self.add_schema(schema)

    def add_schema(self, schema):

        for prop, val in schema.iteritems():
            if prop == 'type':
                self._add_type(val)
            elif prop == 'required':
                self._add_required(val)
            elif prop == 'properties':
                self._add_properties(val, 'add_schema')
            elif prop == 'items':
                self._add_items(val, 'add_schema')
            elif prop not in self._schema:
                self._schema[prop] = val
            elif self._schema[prop] != val:
                raise Exception('schema incompatible')

        # return self for easy method chaining
        return self

    def add_object(self, obj):
        if isinstance(obj, types.DictType):
            self._add_object_object(obj)
        elif isinstance(obj, types.ListType):
            self._add_object_array(obj)
        else:
            self._add_object_basic(obj)

        # return self for easy method chaining
        return self

    def get_type(self):
        schema_type = self._schema.get('type')

        if isinstance(schema_type, set):
            if len(schema_type) == 1:
                (schema_type,) = schema_type
            else:
                schema_type = sorted(schema_type)

        return schema_type

    def get_schema(self):
        schema = copy(self._schema)

        # unpack the type field
        if 'type' in self._schema:
            schema['type'] = self.get_type()

        # call recursively on subschemas if object or array
        if 'object' in self._schema.get('type'):
            schema['properties'] = {}
            for prop, subschema in self._schema['properties'].iteritems():
                schema['properties'][prop] = subschema.get_schema()
            schema['required'] = sorted(self._schema['required'])

        elif 'array' in self._schema.get('type'):
            schema['items'] = \
                [subschema.get_schema() for subschema in self._schema['items']]

        return schema

    def dumps(self, *args, **kwargs):
        # TODO: fix custom JSON encoder
        # kwargs['cls'] = SchemaEncoder
        return json.dumps(self.get_schema(), *args, **kwargs)

    def __eq__(self, other):
        """required for comparing array items to ensure there aren't duplicates
        """
        if not isinstance(other, SchemaGen):
            return False

        # check type first, before recursing the whole of both objects
        if self.get_type() != other.get_type():
            return False

        return self.get_schema() == other.get_schema()

    def __ne__(self, other):
        return not self.__eq__(other)

    # TODO: add sorting methods

    # private methods

    def _add_type(self, val_type):
        if 'type' not in self._schema:
            self._schema['type'] = set()
        if isinstance(val_type, types.StringType):
            self._schema['type'].add(val_type)
        else:
            self._schema['type'] |= set(val_type)

    def _add_required(self, required):
        if 'required' not in self._schema:
            self._schema['required'] = set(required)
        else:
            # use intersection to limit to properties present in both
            self._schema['required'] &= set(required)

    def _add_properties(self, properties, func):
        if 'properties' not in self._schema:
            self._schema['properties'] = defaultdict(lambda: SchemaGen())

        # recursively modify subschemas
        for prop, val in schema['properties'].iteritems():
            getattr(self._schema['properties'][prop], func)(val)

    def _add_items(self, items, func):
        """
        TODO: add _add_items_merge
        """
        self._add_type('array')
        if 'items' not in self._schema:
            self._schema['items'] = []

        for item in array:
            subschema = SchemaGen()
            getattr(subschema, func)(item)

            # only add schema if it's not already there.
            if subschema not in self._schema['items']:
                self._schema['items'].append(subschema)

    def _add_object_object(self, obj):
        self._add_type('object')
        self._add_required(obj.keys())
        self._add_properties(obj, 'add_object')

    def _add_object_array(self, array):
        self._add_type('array')
        self._add_items(array, 'add_object')

    def _add_object_basic(self, val):
        val_type = JS_TYPES[type(val)]
        self._add_type(val_type)


class SchemaEncoder(json.JSONEncoder):
    """subclass of json encoder, used to optimize the SchemaGen.dumps method
    """
    def default(self, obj):
        if isinstance(obj, SchemaGen):
            return obj.dumps()

        if isinstance(obj, set):
            # TODO: this is broken
            return json.JSONEncoder.default(self, sorted(obj))

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
