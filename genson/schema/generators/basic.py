class SchemaGenerator(object):
    KEYWORDS = ('type')
    # JS_TYPE =
    # PYTHON_TYPE =

    @classmethod
    def match_schema(cls, schema):
        return schema.get('type') == cls.JS_TYPE

    @classmethod
    def match_object(cls, obj):
        return isinstance(obj, cls.PYTHON_TYPE)

    def __init__(self, parent_node):
        pass

    def add_schema(self, schema):
        pass

    def add_object(self, obj):
        pass

    def to_schema(self):
        return {'type': self.JS_TYPE}


# Concrete Types

class Null(SchemaGenerator):
    JS_TYPE = 'null'
    PYTHON_TYPE = type(None)


class Boolean(SchemaGenerator):
    JS_TYPE = 'boolean'
    PYTHON_TYPE = bool


class String(SchemaGenerator):
    JS_TYPE = 'string'
    PYTHON_TYPE = (str, type(u''))
