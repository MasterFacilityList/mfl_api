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

    def get_public_fields(self, fields):
        if isinstance(self.instance, list):
            instance_mock = self.instance[0]
        else:
            instance_mock = self.instance

        if not hasattr(instance_mock, 'non_public_fields'):
            return fields

        non_public_fields = instance_mock.non_public_fields
        model_name = instance_mock.__class__.__name__.lower()
        app_label = instance_mock._meta.app_label
        # the view all field model permission must conform to the following
        # naming convention view_all_modelname_fields
        view_fields_perm = "{}.view_all_{}_fields".format(
            app_label, model_name)
        request = self.context.get('request', None)

        if not request.user.has_perm(view_fields_perm):
            all_fields = fields.keys()
            public_fields = list(set(all_fields) - set(non_public_fields))
            return {
                field: fields[field]
                for field in fields if field in public_fields
            }
        else:
            return fields

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
        request = self.context.get('request', None)
        if request is None:
            return origi_fields

        request_method = ""

        if hasattr(request, "method"):
            request_method = request.method

        if request_method != 'GET':
            return origi_fields

        fields = request.QUERY_PARAMS.get('fields', None)
        if isinstance(fields, six.string_types) and fields:
            fields = fields.split(',')
            return {
                field: origi_fields[field]
                for field in origi_fields if field in fields
            }

        return self.get_public_fields(origi_fields)
