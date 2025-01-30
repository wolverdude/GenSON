from .base import SchemaStrategy


class Enum(SchemaStrategy):
    """
    strategy for 'enum' schemas. Merges the 'enum' types into one set and then
    returns a schema with 'enum' set to the corresponding list.
    """

    KEYWORDS = ("enum",)

    def __init__(self, node_class):
        super().__init__(node_class)
        # Use set to easily merge 'enum's from different schemas.
        self._enum = set()
        # Apply different matching logic depending on whether schema exists or
        # not. Give the Enum strategy preference over other strategies. So
        # there's no way the Enum will get created unless it was explicitly
        # asked for by a schema, and this behavior is not order- or
        # type-dependent.
        self.match_object = self._instance_match_object

    @staticmethod
    def match_object(cls, obj):
        # Exclude the strategy from the basic object matching. It must be
        # explicitly selected by a schema.
        return False

    def _instance_match_object(self, obj):
        # The strategy is selected by a schema. Give the Enum strategy
        # preference over all other strategies.
        return True

    @staticmethod
    def match_schema(schema):
        return "enum" in schema

    def add_schema(self, schema):
        super().add_schema(schema)
        if self._enum == set():
            self._enum = set(schema.get("enum"))
        elif "enum" in schema:
            self._enum.update(schema["enum"])

    def add_object(self, obj):
        super().add_object(obj)
        # Add only scalar types. Technically, the JSON-Schema spec allows
        # any type in an enum list, but using objects and lists is a very
        # rare use-case.
        if obj is not None and type(obj) not in [bool, str, int, float]:
            raise TypeError(f"Unsupported enum type of {type(obj)}."
                            "Scalar type is expected.")
        # Convert to list to unify processing of string and other types.
        self._enum.update([obj])

    def to_schema(self):
        schema = super().to_schema()
        # Revert set back to list
        schema["enum"] = list(self._enum)
        return schema
