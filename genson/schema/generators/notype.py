from warnings import warn
from .basic import SchemaGenerator


class NoType(SchemaGenerator):

    @classmethod
    def match_schema(cls, schema):
        return 'type' not in schema

    @classmethod
    def match_object(cls, obj):
        return False

    def add_schema(self, schema):
        warn(('Schema with no type added. This may lead to an '
              'incompletely-merged and over-permissive result schema. '
              'schema: {!r}').format(schema))

        SchemaGenerator.add_schema(self, schema)

    def to_schema(self):
        return {}
