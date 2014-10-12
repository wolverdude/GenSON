import types
import json
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

    def __init__(self):
        self._schema = {}

    def add_object(self, obj):
        if isinstance(obj, types.DictType):
            self._gen_object(obj)
        elif isinstance(obj, types.ListType):
            self._gen_array(obj)
        else:
            self._gen_basic(obj)

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
        schema = {}

        # unpack the type field
        if 'type' in self._schema:
            schema['type'] = self.get_type()

        # call recursively on subschemas if object or array
        if schema.get('type') == 'object':
            schema['properties'] = {}
            for prop, subschema in self._schema['properties'].iteritems():
                schema['properties'][prop] = subschema.get_schema()
            schema['required'] = sorted(self._schema['required'])

        elif schema.get('type') == 'array':
            schema['items'] = \
                [subschema.get_schema() for subschema in self._schema['items']]

        return schema

    def dumps(self, *args, **kwargs):
        kwargs['cls'] = SchemaEncoder
        return json.dumps(self._schema, *args, **kwargs)

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

    def _gen_object(self, obj):
        self._add_type('object')
        if 'properties' not in self._schema:
            self._schema['properties'] = defaultdict(lambda: SchemaGen())

        if 'required' not in self._schema:
            self._schema['required'] = set(obj.keys())
        else:
            # use intersection to limit to properties present in both
            self._schema['required'] &= set(obj.keys())

        # recursively modify subschemas
        for prop, val in obj.iteritems():
            self._schema['properties'][prop].add_object(val)

    def _gen_array(self, array):
        """
        TODO: add _get_array_type_merge
        """
        self._add_type('array')
        if 'items' not in self._schema:
            self._schema['items'] = []

        for item in array:
            subschema = SchemaGen()
            subschema.add_object(item)

            # only add schema if it's not already there.
            if subschema not in self._schema['items']:
                self._schema['items'].append(subschema)

    def _gen_basic(self, val):
        val_type = JS_TYPES[type(val)]
        self._add_type(val_type)

    def _add_type(self, val_type):
        if 'type' not in self._schema:
            self._schema['type'] = set()
        self._schema['type'].add(val_type)


class SchemaEncoder(json.JSONEncoder):
    """subclass of json encoder, used to optimize the SchemaGen.dumps method
    """
    def default(self, obj):
        if isinstance(obj, SchemaGen):
            return obj.dumps()

        if isinstance(obj, set):
            return json.JSONEncoder.default(self, sorted(obj))

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
