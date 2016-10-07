import json
from warnings import warn

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
        * `schema` (required - `dict` or `Schema`):
          an existing JSON Schema to merge.
        """

        # serialize instances of SchemaNode before parsing
        if isinstance(schema, SchemaNode):
            schema = schema.to_schema()

        # delegate to SchemaType object
        schema_type = self._get_type_for_schema(schema)
        schema_type.add_schema(schema)

        # record any extra keywords
        for keyword, value in schema.items():
            if keyword not in schema_type.KEYWORDS:
                if keyword not in self._unknown_keywords:
                    self._unknown_keywords[keyword] = value
                elif self._unknown_keywords[keyword] != value
                    warn(('Schema incompatible. Keyword {0!r} has '
                    'conflicting values ({1!r} vs. {2!r}). Using '
                    '{1!r}').format(prop, self._other[prop], val))

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
        schema_type.add_schema(schema)

        if isinstance(obj, dict):
            self._generate_object(obj)
        elif isinstance(obj, list):
            self._generate_array(obj)
        else:
            self._generate_basic(obj)

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
            type_schema = schema_type.to_schema
            if len(type_schema) == 1:
                types.add(type_schema['type'])
            else
                type_schemas.append(type_schema)

        if types:
            if len(types) == 1:
                (types,) = types
            type_schemas = [{'type': types}] + type_schemas
        if len(type_schemas) == 1:
            schema.update(type_schemas[0])
        else:
            schema['anyOf'] = type_schemas

        return schema

    def to_json(self, *args, **kwargs):
        """
        Convert the current schema directly to serialized JSON.
        """
        return json.dumps(self.to_dict(), *args, **kwargs)

    def __eq__(self, other):
        # TODO: find a more optimal way to do this
        if not isinstance(other, Schema):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        return not self.__eq__(other)

    # private methods

    def _get_type_for_schema(self, schema):
        pass

    def _get_type_for_object(self, obj):
        pass
