from builtins import super
from warnings import warn
from .base import SchemaGenerator, TypedSchemaGenerator


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

        super().add_schema(schema)


class Null(TypedSchemaGenerator):
    JS_TYPE = 'null'
    PYTHON_TYPE = type(None)


class Boolean(TypedSchemaGenerator):
    JS_TYPE = 'boolean'
    PYTHON_TYPE = bool


class String(TypedSchemaGenerator):
    JS_TYPE = 'string'
    PYTHON_TYPE = (str, type(u''))


class Number(SchemaGenerator):
    JS_TYPES = ('integer', 'number')
    PYTHON_TYPES = (int, float)

    @classmethod
    def match_schema(cls, schema):
        return schema.get('type') in cls.JS_TYPES

    @classmethod
    def match_object(cls, obj):
        return type(obj) in cls.PYTHON_TYPES

    def __init__(self, parent_node):
        super().__init__(parent_node)
        self._type = 'integer'

    def add_schema(self, schema):
        super().add_schema(schema)
        if schema.get('type') == 'number':
            self._type = 'number'

    def add_object(self, obj):
        if isinstance(obj, float):
            self._type = 'number'

    def to_schema(self):
        schema = super().to_schema()
        schema['type'] = self._type
        return schema
