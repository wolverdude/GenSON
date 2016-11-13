from .list import List
from .tuple import Tuple

__all__ = types = [
    List,
    Tuple,
]


def add_type(schema_type):
    # TODO: validate schema type
    types.append(schema_type)
