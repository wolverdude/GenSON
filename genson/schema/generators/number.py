class Number(object):
    KEYWORDS = ('type')
    JS_TYPES = ('integer', 'number')
    PYTHON_TYPES = (int, float)

    @classmethod
    def match_schema(cls, schema):
        return schema.get('type') in cls.JS_TYPES

    @classmethod
    def match_object(cls, obj):
        return type(obj) in cls.PYTHON_TYPES

    def __init__(self, parent_node):
        self._type = 'integer'

    def add_schema(self, schema):
        if schema.get('type') == 'number':
            self._type = 'number'

    def add_object(self, obj):
        if isinstance(obj, float):
            self._type = 'number'

    def to_schema(self):
        return {'type': self._type}
