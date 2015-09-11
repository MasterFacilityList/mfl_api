import six

from django.utils import timezone


class PartialResponseMixin(object):

    def strip_fields(self, request, origi_fields):
        """
        Fetch a subset of fields from the serializer determined by the
        request's ``fields`` query parameter.

        This is an initial implementation that does not handle:
          - nested relationships
          - rejection of unknown fields (currently ignoring unknown fields)
          - wildcards
          - e.t.c
        """
        if request is None:
            return origi_fields

        request_method = ""

        if hasattr(request, "method"):
            request_method = request.method

        if request_method != 'GET':
            return origi_fields

        fields = request.query_params.get('fields', None)
        if isinstance(fields, six.string_types) and fields:
            fields = fields.split(',')
            return {
                field: origi_fields[field]
                for field in origi_fields if field in fields
            }
        return origi_fields


class AbstractFieldsMixin(PartialResponseMixin):

    """
    Injects the fields in the abstract base model as a model
    instance is being saved.
    """

    def create(self, validated_data):
        """`created` and `created_by` are only mutated if they are null"""
        if not validated_data.get('created', None):
            validated_data['created'] = timezone.now()

        validated_data['updated'] = timezone.now()

        if validated_data.get('created_by', None) is None:
            validated_data['created_by'] = self.context['request'].user

        if not validated_data.get('updated_by', None):
            validated_data['updated_by'] = self.context['request'].user

        return self.Meta.model.objects.create(**validated_data)

    def get_fields(self):
        """Overridden to take advantage of partial response"""
        origi_fields = super(AbstractFieldsMixin, self).get_fields()
        request = self.context.get('request', None)
        return self.strip_fields(request, origi_fields)
