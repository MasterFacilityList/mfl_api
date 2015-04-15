from django.utils import timezone


class AbstractFieldsMixin(object):
    """
    Injects the fields in the abstract base model as a model
    instance is being saved.
    """
    def __init__(self, *args, **kwargs):
        super(AbstractFieldsMixin, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        """`created` and `created_by` are only mutated if they are null"""
        if not validated_data.get('created', None):
            validated_data['created'] = timezone.now()

        validated_data['updated'] = timezone.now()

        if not validated_data.get('created_by', None):
            validated_data['created_by'] = self.context['request'].user

        validated_data['updated_by'] = self.context['request'].user

        return self.Meta.model.objects.create(**validated_data)
