from .base import SchemaStrategy


class Enum(SchemaStrategy):
    """
    strategy for 'enum' schemas. Merges the 'enum' types into one set and then
    returns a schema with 'enum' set to the corresponding list.
    """

    KEYWORDS = ("enum",)

    def init(self, node_class):
        super().init(node_class)
        # Use set to easily merge 'enum's from different schemas.
        self._enum = set()

    @staticmethod
    def match_schema(schema):
        return "enum" in schema

    @classmethod
    def match_object(cls, obj):
        # Match any enum object. Enum is not in basic strategies.
        return True

    def add_schema(self, schema):
        super().add_schema(schema)
        if self._enum == set():
            self._enum = set(schema.get("enum"))
        elif "enum" in schema:
            self._enum.update(schema["enum"])

    def add_object(self, obj):
        # Convert to list to unify processing of iterables and other types.
        obj_list = list(obj)
        for item in obj_list:
            item_type = type(item)
            if item_type in [bool, str, int, float]:
                self._enum.add(item)
            elif item is None:
                self._enum.add("null")
            else:
                raise TypeError(f"Unsupported enum type: {type(item_type)}")

    def to_schema(self):
        schema = super().to_schema()
        # Revert set back to list
        schema["enum"] = list(self._enum)
        return schema