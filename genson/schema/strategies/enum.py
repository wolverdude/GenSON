from .base import SchemaStrategy


class Enum(SchemaStrategy):
    """
    enum schema strategy
    """
    KEYWORDS = ("enum",)

    @classmethod
    def match_schema(cls, schema):
        return "enum" in schema

    @staticmethod
    def match_object(obj):
        # Match any enum object. Enum is not in basic strategies.
        return True

    def to_schema(self):
        schema = super().to_schema()
        if self._enum:
            schema["enum"] = self._enum
        return schema

    def init(self, node_class):
        super().init(node_class)
        self._enum = []

    def add_object(self, obj):
        if isinstance(obj, list):
            self._enum.extend(obj)
        else:
            self._enum.append(obj)