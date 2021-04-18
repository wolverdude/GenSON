from .base import SchemaStrategy


class Enum(SchemaStrategy):
    """
    strategy for 'enum' schemas. Merges the 'enum' types into one set and then
    returns a schema with 'enum' set to the corresponding list.
    """
    KEYWORDS = ('enum', )

    def __init__(self, node_class):
        super().__init__(node_class)
        # Use set to easily merge 'enum's from different schemas.
        self._enum = set()

    @staticmethod
    def match_schema(schema):
        return 'enum' in schema

    @classmethod
    def match_object(cls, obj):
        return False

    def add_schema(self, schema):
        super().add_schema(schema)
        if self._enum == set():
            self._enum = set(schema.get('enum'))
        elif 'enum' in schema:
            self._enum.update(schema['enum'])

    def to_schema(self):
        schema = super().to_schema()
        # Revert set back to list
        schema['enum'] = list(self._enum)
        return schema
