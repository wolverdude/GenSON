from .generators import GENERATORS, Typeless


class SchemaGenerationError(RuntimeError):
    pass


class SchemaNode(object):
    """
    Basic schema generator class. SchemaNode objects can be loaded
    up with existing schemas and objects before being serialized.
    """
    generator_classes = GENERATORS

    def __init__(self):
        self._schema_generators = []

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

        for subschema in self._get_subschemas(schema):
            # delegate to SchemaType object
            schema_generator = self._get_generator_for_schema(subschema)
            schema_generator.add_schema(subschema)

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
            (result_schema,) = generated_schemas
        elif generated_schemas:
            result_schema = {'anyOf': generated_schemas}
        else:
            result_schema = {}

        return result_schema

    def __len__(self):
        return len(self._schema_generators)

    def __eq__(self, other):
        # TODO: find a more optimal way to do this
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False

        return self.to_schema() == other.to_schema()

    def __ne__(self, other):
        return not self.__eq__(other)

    # private methods

    def _get_subschemas(self, schema):
        if 'anyOf' in schema:
            return schema['anyOf']
        elif isinstance(schema.get('type'), list):
            other_keys = dict(schema)
            del other_keys['type']
            return [dict(type=tipe, **other_keys) for tipe in schema['type']]
        else:
            return [schema]

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
        for schema_generator_class in self.generator_classes:
            if getattr(schema_generator_class, 'match_' + kind)(schema_or_obj):
                schema_generator = schema_generator_class(type(self))

                # incorporate typeless generator if it exists
                if self._schema_generators and \
                        isinstance(self._schema_generators[-1], Typeless):
                    typeless = self._schema_generators.pop()
                    schema_generator.add_schema(typeless.to_schema())

                self._schema_generators.append(schema_generator)
                return schema_generator

        # no match found, if typeless add to first generator
        if kind == 'schema' and Typeless.match_schema(schema_or_obj):
            if not self._schema_generators:
                self._schema_generators.append(Typeless(type(self)))
            schema_generator = self._schema_generators[0]
            return schema_generator

        # no match found, raise an error
        raise SchemaGenerationError(
            'Could not find matching type for {0}: {1!r}'.format(
                kind, schema_or_obj))
