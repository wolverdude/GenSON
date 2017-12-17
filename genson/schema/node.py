import json
from warnings import warn
from .generators import GENERATORS


class InvalidSchemaError(RuntimeError):
    pass


class SchemaNode(object):
    """
    Basic schema generator class. SchemaNode objects can be loaded
    up with existing schemas and objects before being serialized.
    """

    def __init__(self):
        self._schema_generators = []
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

        # delegate to SchemaType object
        schema_generator = self._get_generator_for_schema(schema)
        schema_generator.add_schema(schema)

        # record any extra keywords
        for keyword, value in schema.items():
            if keyword in schema_generator.KEYWORDS:
                continue
            elif keyword not in self._unknown_keywords:
                self._unknown_keywords[keyword] = value
            elif self._unknown_keywords[keyword] != value:
                warn(('Schema incompatible. Keyword {0!r} has conflicting '
                      'values ({1!r} vs. {2!r}). Using {1!r}').format(
                          keyword, self._unknown_keywords[keyword], value))

        # return self for easy method chaining
        return self

    def add_object(self, obj):
        """
        Modify the schema to accomodate an object.

        arguments:
        * `obj` (required - `dict`):
          a JSON object to use in generating the schema.
        """

        # delegate to SchemaType object
        schema_generator = self._get_generator_for_object(obj)
        schema_generator.add_object(obj)

        # return self for easy method chaining
        return self

    def to_schema(self):
        """
        Convert the current schema to a `dict`.
        """
        # start with unknown keywords
        result_schema = dict(self._unknown_keywords)

        types = set()
        generated_schemas = []
        for schema_generator in self._schema_generators:
            generated_schema = schema_generator.to_schema()
            if len(generated_schema) == 1 and 'type' in generated_schema:
                types.add(generated_schema['type'])
            else:
                generated_schemas.append(generated_schema)

        if types:
            if len(types) == 1:
                (types,) = types
            else:
                types = sorted(types)
            generated_schemas = [{'type': types}] + generated_schemas
        if len(generated_schemas) == 1:
            result_schema.update(generated_schemas[0])
        elif generated_schemas:
            result_schema['anyOf'] = generated_schemas

        return result_schema

    def to_dict(self, recurse='DEPRECATED'):
        warn('#to_dict is deprecated in v1.0, and it may be removed in '
             'future versions. Use #to_schema instead.',
             PendingDeprecationWarning)
        if recurse != 'DEPRECATED':
            warn('the `recurse` option for #to_dict does nothing in v1.0',
                 DeprecationWarning)
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

    def _get_generator_for_schema(self, schema):
        return self._get_generator_for_('schema', schema)

    def _get_generator_for_object(self, obj):
        return self._get_generator_for_('object', obj)

    def _get_generator_for_(self, kind, schema_or_obj):
        # check existing types
        for schema_generator in self._schema_generators:
            if getattr(schema_generator, 'match_' + kind)(schema_or_obj):
                return schema_generator

        # check all potential types
        for schema_generator_class in GENERATORS:
            if getattr(schema_generator_class, 'match_' + kind)(schema_or_obj):
                schema_generator = schema_generator_class(self)
                self._schema_generators.append(schema_generator)
                return schema_generator

        # no match found, raise an error
        raise InvalidSchemaError(
            'Could not find matching type for {0}: {1!r}'.format(
                kind, schema_or_obj))
