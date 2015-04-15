from __future__ import unicode_literals

from collections import OrderedDict
from django.utils.encoding import force_text
from rest_framework.metadata import SimpleMetadata


class CustomMetadata(SimpleMetadata):
    """
    Based on the implementation of SimpleMetaData in DRF v3.1
    """

    def get_field_info(self, field):
        """
        Given an instance of a serializer field, return a dictionary
        of metadata about it.

        This differs from the base class method in its approach to choices.
        The base class method will inline choices. The definition of choices
        is extensive, so that it may end up inlining the contents of an entire
        related table.
        """
        field_info = OrderedDict()
        field_info['type'] = self.label_lookup[field]
        field_info['required'] = getattr(field, 'required', False)

        attrs = [
            'read_only', 'label', 'help_text',
            'min_length', 'max_length',
            'min_value', 'max_value'
        ]

        for attr in attrs:
            value = getattr(field, attr, None)
            if value is not None and value != '':
                field_info[attr] = force_text(value, strings_only=True)

        # TODO Proper handling of FKs and M2Ms

        return field_info
