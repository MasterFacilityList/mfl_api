from django.db.models import Field


class SequenceField(Field):
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        super(SequenceField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(SequenceField, self).deconstruct()
        # lacks 'kwargs['primary_key'] = True', unlike AutoField
        return name, path, args, kwargs

    def get_internal_type(self):
        return "SequenceField"

    def to_python(self, value):
        return int(value)

    def db_type(self, connection):
        return 'serial'

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
            # avoid the PK validation of AutoField
        return value

    def get_prep_value(self, value):
        value = super(SequenceField, self).get_prep_value(value)
        if value is None or value == '':
            return None
        return int(value)

    def contribute_to_class(self, cls, name):
        self.set_attributes_from_name(name)
        self.model = cls
        cls._meta.add_field(self)
