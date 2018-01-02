from . import base
from genson import Schema, SchemaGenerationError


class TestMisuse(base.GensonTestCase):

    def test_schema_with_bad_type_error(self):
        with self.assertRaises(SchemaGenerationError):
            self.add_schema({'type': 'african swallow'})

    @base.minimum_python(3, 3)
    def test_to_dict_pending_deprecation_warning(self):
        with self.assertWarns(PendingDeprecationWarning):
            s = Schema()
        with self.assertWarns(PendingDeprecationWarning):
            s.add_object('I fart in your general direction!')
            s.to_dict()

    @base.minimum_python(3, 3)
    def test_recurse_deprecation_warning(self):
        with self.assertWarns(DeprecationWarning):
            s = Schema()
            s.add_object('Go away or I shall taunt you a second time!')
            s.to_dict(recurse=True)

    @base.minimum_python(3, 3)
    def test_incompatible_schema_warning(self):
        with self.assertWarns(UserWarning):
            self.add_schema({'type': 'string', 'length': 5})
            self.add_schema({'type': 'string', 'length': 7})
