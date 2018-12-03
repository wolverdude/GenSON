from . import base
from genson import Schema, SchemaGenerationError


class TestMisuse(base.SchemaBuilderTestCase):

    def test_schema_with_bad_type_error(self):
        with self.assertRaises(SchemaGenerationError):
            self.add_schema({'type': 'african swallow'})

    @base.only_for_python_version('>=3.3')
    def test_to_dict_pending_deprecation_warning(self):
        with self.assertWarns(PendingDeprecationWarning):
            builder = Schema()
        with self.assertWarns(PendingDeprecationWarning):
            builder.add_object('I fart in your general direction!')
            builder.to_dict()

    @base.only_for_python_version('>=3.3')
    def test_recurse_deprecation_warning(self):
        with self.assertWarns(DeprecationWarning):
            builder = Schema()
            builder.add_object('Go away or I shall taunt you a second time!')
            builder.to_dict(recurse=True)

    @base.only_for_python_version('>=3.3')
    def test_incompatible_schema_warning(self):
        with self.assertWarns(UserWarning):
            self.add_schema({'type': 'string', 'length': 5})
            self.add_schema({'type': 'string', 'length': 7})
