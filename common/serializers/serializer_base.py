import six

from django.utils import timezone


class AbstractFieldsMixin(object):

    """
    Injects the fields in the abstract base model as a model
    instance is being saved.
    """

    def create(self, validated_data):
        """`created` and `created_by` are only mutated if they are null"""
        if not validated_data.get('created', None):
            validated_data['created'] = timezone.now()

        validated_data['updated'] = timezone.now()

        if not validated_data.get('created_by', None):
            validated_data['created_by'] = self.context['request'].user

        validated_data['updated_by'] = self.context['request'].user

        return self.Meta.model.objects.create(**validated_data)

    def get_fields(self):
        """
        Fetch a subset of fields from the serializer determined by the
        request's ``fields`` query parameter.

        This is an initial implementation that does not handle:
          - nested relationships
          - rejection of unknown fields (currently ignoring unknown fields)
          - wildcards
          - e.t.c
        """
        origi_fields = super(AbstractFieldsMixin, self).get_fields()
        request = self.context['request']

        request_method = ""
        try:
            request_method = request.method
        except AttributeError:
            request.get('REQUEST_METHOD', None)

        if request_method != 'GET':
            return origi_fields

        fields = request.QUERY_PARAMS.get('fields', None)
        if isinstance(fields, six.string_types) and fields:
            fields = fields.split(',')
            return {
                field: origi_fields[field]
                for field in origi_fields if field in fields
            }
        return origi_fields
