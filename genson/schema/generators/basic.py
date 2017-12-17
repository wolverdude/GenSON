from warnings import warn


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
        self._unknown_keywords = {}

    def add_schema(self, schema):
        # record any extra keywords
        for keyword, value in schema.items():
            if keyword in self.KEYWORDS:
                continue
            elif keyword not in self._unknown_keywords:
                self._unknown_keywords[keyword] = value
            elif self._unknown_keywords[keyword] != value:
                warn(('Schema incompatible. Keyword {0!r} has conflicting '
                      'values ({1!r} vs. {2!r}). Using {1!r}').format(
                          keyword, self._unknown_keywords[keyword], value))

    def add_object(self, obj):
        pass

    def to_schema(self):
        return dict(type=self.JS_TYPE, **self._unknown_keywords)


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
