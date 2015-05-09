from __future__ import unicode_literals

import logging

from collections import OrderedDict
from django.utils.encoding import force_text
from rest_framework.metadata import SimpleMetadata

from rest_framework.request import clone_request
from rest_framework.reverse import reverse

LOGGER = logging.getLogger(__name__)


class CustomMetadata(SimpleMetadata):
    """
    Based on the implementation of SimpleMetaData in DRF v3.1
    """
    def determine_metadata(self, request, view):
        self.request = request
        self.view = view
        return super(CustomMetadata, self).determine_metadata(request, view)

    def determine_actions(self, request, view):
        """
        For generic class based views we return information about
        the fields that are accepted for 'PUT' and 'POST' methods.
        """
        actions = {}
        for method in set(['PUT', 'POST']) & set(view.allowed_methods):
            view.request = clone_request(request, method)
            serializer = view.get_serializer()
            actions[method] = self.get_serializer_info(serializer)
            view.request = request

        return actions

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

        if hasattr(field, 'queryset'):
            # Late import ( cyclic import issues )
            from .utilities.metadata_helpers import MODEL_VIEW_DICT
            assert hasattr(field.queryset, 'model'), \
                '{} has no queryset'.format(field)
            field_info['relational_choices'] = [
                {
                    'value': reverse(
                        MODEL_VIEW_DICT[field.queryset.model]['list_url'],
                        request=self.request
                    ),
                    'display_name':
                        field.queryset.model._meta.verbose_name_plural
                }
            ]
        elif hasattr(field, 'choices'):
            field_info['choices'] = [
                {
                    'value': choice_value,
                    'display_name': force_text(choice_name, strings_only=True)
                }
                for choice_value, choice_name in field.choices.items()
            ]

        return field_info
