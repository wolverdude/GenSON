from sys import intern

class Py2Key:
    """Custom key class for 'sorted' to sort a list of different types."""

    __slots__ = ("value", "typestr")

    def __init__(self, value):
        self.value = value
        self.typestr = intern(type(value).__name__)

    def __lt__(self, other):
        try:
            return self.value < other.value
        except TypeError:
            return self.typestr < other.typestr


def sort_lists_in_schema(schema, sorted_key):
    stack = []
    stack.append(schema)
    while stack:
        node = stack.pop()

        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, dict):
                    stack.append(v)
                elif isinstance(v, list):
                    node[k] = sorted(v, key=sorted_key)
                    stack.append(v)

        if isinstance(node, list):
            for position, list_item in enumerate(node):
                if isinstance(list_item, dict):
                    stack.append(list_item)
                if isinstance(list_item, list):
                    node[position] = sorted(list_item, key=sorted_key)
                    stack.append(list_item)