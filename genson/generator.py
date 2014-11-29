import json
from collections import defaultdict

JS_TYPES = {
    dict: 'object',
    list: 'array',
    str: 'string',
    type(u''): 'string',
    int: 'integer',
    float: 'number',
    bool: 'boolean',
    type(None): 'null',
}


class Schema(object):
    """
    Basic schema generator class. Schema objects can be loaded up
    with existing schemas and objects before being serialized.
    """

    def __init__(self, merge_arrays=True):
        """
        Builds a schema generator object.

        arguments:
        * `merge_arrays` (default `True`): Assume all array items share
          the same schema (as they should). The alternate behavior is to
          create a different schema for each item in every array.
        """
        self._type = set()
        self._required = None
        self._properties = defaultdict(lambda: Schema())
        self._items = []
        self._other = {}
        self.merge_arrays = merge_arrays

    def add_schema(self, schema):
        """
        Merges in an existing schema.

        arguments:
        * `schema` (required - `dict` or `Schema`):
          an existing JSON Schema to merge.
        """

        # serialize instances of Schema before parsing
        if isinstance(schema, Schema):
            schema = schema.to_dict()

        # parse properties and add them individually
        for prop, val in schema.items():
            if prop == 'type':
                self._add_type(val)
            elif prop == 'required':
                self._add_required(val)
            elif prop == 'properties':
                self._add_properties(val, 'add_schema')
            elif prop == 'items':
                self._add_items(val, 'add_schema')
            elif prop not in self._other:
                self._other[prop] = val
            elif self._other[prop] != val:
                raise Exception('schema incompatible')

        # make sure the 'required' key gets set regardless
        if 'required' not in schema:
            self._add_required([])

        # return self for easy method chaining
        return self

    def add_object(self, obj):
        """
        Modify the schema to accomodate an object.

        arguments:
        * `obj` (required - `dict`):
          a JSON object to use in generate the schema.
        """

        if isinstance(obj, dict):
            self._generate_object(obj)
        elif isinstance(obj, list):
            self._generate_array(obj)
        else:
            self._generate_basic(obj)

        # return self for easy method chaining
        return self

    def to_dict(self, recurse=True):
        """
        Convert the current schema to a `dict`.
        """
        # start with existing fields
        schema = dict(self._other)

        # unpack the type field
        if self._type:
            schema['type'] = self._get_type()

        # call recursively on subschemas if object or array
        if 'object' in self._type:
            schema['properties'] = self._get_properties(recurse)
            if self._required:
                schema['required'] = self._get_required()

        elif 'array' in self._type:
            schema['items'] = self._get_items(recurse)

        return schema

    def to_json(self, *args, **kwargs):
        """
        Convert the current schema directly to serialized JSON.
        """
        return json.dumps(self.to_dict(), *args, **kwargs)

    def __eq__(self, other):
        """required for comparing array items to ensure there aren't duplicates
        """
        if not isinstance(other, Schema):
            return False

        # check type first, before recursing the whole of both objects
        if self._get_type() != other._get_type():
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        return not self.__eq__(other)

    # private methods

    # getters

    def _get_type(self):
        schema_type = self._type | set()  # get a copy

        # remove any redundant integer type
        if 'integer' in schema_type and 'number' in schema_type:
            schema_type.remove('integer')

        # unwrap if only one item, else convert to array
        if len(schema_type) == 1:
            (schema_type,) = schema_type
        else:
            schema_type = sorted(schema_type)

        return schema_type

    def _get_required(self):
        return sorted(self._required) if self._required else []

    def _get_properties(self, recurse=True):
        if not recurse:
            return dict(self._properties)

        properties = {}
        for prop, subschema in self._properties.items():
            properties[prop] = subschema.to_dict()
        return properties

    def _get_items(self, recurse=True):
        if not recurse:
            return list(self._items)

        return [subschema.to_dict() for subschema in self._items]

    # setters

    def _add_type(self, val_type):
        if isinstance(val_type, (str, type(u''))):
            self._type.add(val_type)
        else:
            self._type |= set(val_type)

    def _add_required(self, required):
        if self._required is None:
            # if not already set, set to this
            self._required = set(required)
        else:
            # use intersection to limit to properties present in both
            self._required &= set(required)

    def _add_properties(self, properties, func):
        # recursively modify subschemas
        for prop, val in properties.items():
            getattr(self._properties[prop], func)(val)

    def _add_items(self, items, func):
        if self.merge_arrays:
            self._add_items_merge(items, func)
        else:
            self._add_items_sep(items, func)

    def _add_items_merge(self, items, func):
        if items:
            if not self._items:
                self._items.append(Schema())

            method = getattr(self._items[0], func)
            for item in items:
                method(item)

    def _add_items_sep(self, items, func):
        for item in items:
            subschema = Schema()
            getattr(subschema, func)(item)

            # only add schema if it's not already there.
            if subschema not in self._items:
                self._items.append(subschema)

    # generate from object

    def _generate_object(self, obj):
        self._add_type('object')
        self._add_required(obj.keys())
        self._add_properties(obj, 'add_object')

    def _generate_array(self, array):
        self._add_type('array')
        self._add_items(array, 'add_object')

    def _generate_basic(self, val):
        val_type = JS_TYPES[type(val)]
        self._add_type(val_type)
