import json
from warnings import warn
from .schema_types import SCHEMA_TYPES


class SchemaNode(object):
    """
    Basic schema generator class. SchemaNode objects can be loaded
    up with existing schemas and objects before being serialized.
    """

    def __init__(self):
        self._schema_types = []
        self._unknown_keywords = {}

    def add_schema(self, schema):
        """
        Merges in an existing schema.

        arguments:
        * `schema` (required - `dict` or `SchemaNode`):
          an existing JSON Schema to merge.
        """

        # serialize instances of SchemaNode before parsing
        if isinstance(schema, SchemaNode):
            schema = schema.to_schema()

        if 'type' not in schema:
            warn('Given schema has no "type" key: {0!r}')
            return

        # delegate to SchemaType object
        schema_type = self._get_type_for_schema(schema)
        schema_type.add_schema(schema)

        # record any extra keywords
        for keyword, value in schema.items():
            if keyword in schema_type.KEYWORDS:
                continue
            elif keyword not in self._unknown_keywords:
                self._unknown_keywords[keyword] = value
            elif self._unknown_keywords[keyword] != value:
                warn(('Schema incompatible. Keyword {0!r} has '
                      'conflicting values ({1!r} vs. {2!r}). Using '
                      '{1!r}').format(keyword, self._other[keyword], value))

        # return self for easy method chaining
        return self

    def add_object(self, obj):
        """
        Modify the schema to accomodate an object.

        arguments:
        * `obj` (required - `dict`):
          a JSON object to use in generate the schema.
        """

        # delegate to SchemaType object
        schema_type = self._get_type_for_object(obj)
        schema_type.add_object(obj)

        # return self for easy method chaining
        return self

    def to_schema(self):
        """
        Convert the current schema to a `dict`.
        """
        # start with unknown keywords
        schema = dict(self._unknown_keywords)

        types = set()
        type_schemas = []
        for schema_type in self._schema_types:
            type_schema = schema_type.to_schema()
            if len(type_schema) == 1:
                types.add(type_schema['type'])
            else:
                type_schemas.append(type_schema)

        if types:
            if len(types) == 1:
                (types,) = types
            else:
                types = sorted(types)
            type_schemas = [{'type': types}] + type_schemas
        if len(type_schemas) == 1:
            schema.update(type_schemas[0])
        elif type_schemas:
            schema['anyOf'] = type_schemas

        return schema

    def to_dict(self, recurse=True):
        warn('#to_dict is deprecated in v1.0, and it may soon be removed')
        if recurse is not True:
            warn('the `recurse` option for #to_dict does nothing in v1.0')
        return self.to_schema()

    def to_json(self, *args, **kwargs):
        """
        Convert the current schema directly to serialized JSON.
        """
        return json.dumps(self.to_schema(), *args, **kwargs)

    def __eq__(self, other):
        # TODO: find a more optimal way to do this
        if self == other:
            return True
        if not isinstance(other, SchemaNode):
            return False

        return self.to_schema() == other.to_schema()

    def __ne__(self, other):
        return not self.__eq__(other)

    # private methods

    def _get_type_for_schema(self, schema):
        return self._get_type_for_('schema', schema)

    def _get_type_for_object(self, obj):
        return self._get_type_for_('object', obj)

    def _get_type_for_(self, kind, schema_or_obj):
        # check existing types
        for schema_type in self._schema_types:
            if getattr(schema_type, 'match_' + kind)(schema_or_obj):
                return schema_type

        # check all potential types
        for schema_type_class in SCHEMA_TYPES:
            if getattr(schema_type_class, 'match_' + kind)(schema_or_obj):
                schema_type = schema_type_class(self)
                self._schema_types.append(schema_type)
                return schema_type

        # no match found, raise an error
        raise RuntimeError(
            'Could not find matching type for {0}: {1!r}'.format(
                kind, schema_or_obj))
