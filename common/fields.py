from django.db.models import AutoField


class SequenceField(AutoField):
    """Overrides the parts of AutoField that force it to be a PK"""
    def __init__(self, *args, **kwargs):
        super(SequenceField, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        """Shut up '(fields.E100) AutoFields must set primary_key=True.'"""
        errors = super(AutoField, self).check(**kwargs)
        return errors

    def deconstruct(self):
        name, path, args, kwargs = super(AutoField, self).deconstruct()
        # lacks 'kwargs['primary_key'] = True', unlike AutoField
        return name, path, args, kwargs

    def get_internal_type(self):
        return "SequenceField"

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
            # avoid the PK validation of AutoField
        return value

    def contribute_to_class(self, cls, name, **kwargs):
        """Stop enforcing the 'one autofield per class' validation"""
        super(AutoField, self).contribute_to_class(cls, name, **kwargs)
