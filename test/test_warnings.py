from . import base


class TestWarnings(base.SchemaTestCase):

    def test_schema_with_no_type_warning(self):
        with self.assertWarns(UserWarning):
            self.add_schema({"items": [{'type': 'string'}]})

    def test_to_dict_pending_deprecation_warning(self):
        with self.assertWarns(PendingDeprecationWarning):
            self.add_object('I fart in your general direction!')
            self._schema.to_dict()

    def test_recurse_deprecation_warning(self):
        with self.assertWarns(DeprecationWarning):
            self.add_object('Go away or I shall taunt you a second time!')
            self._schema.to_dict(recurse=True)

    def test_incompatible_schema_warning(self):
        with self.assertWarns(UserWarning):
            self.add_schema({'type': 'string', 'length': 5})
            self.add_schema({'type': 'string', 'length': 7})
