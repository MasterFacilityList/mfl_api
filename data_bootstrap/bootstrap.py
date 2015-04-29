import json
import logging

from collections import defaultdict
from django.db.models import get_model
from django.db import transaction

from common.fields import SequenceField

LOGGER = logging.getLogger(__name__)


def _retrieve_existing_model_instance(model_cls, field_data):
    """RETRIEVE an existing model instance ( mainly used to resolve FKs )"""
    # to prevent any modifications making their way back to
    # the original dict
    assert isinstance(field_data, dict)
    try:
        instance = model_cls.objects.get(**field_data)
    except:
        LOGGER.error(
            'Unable to get an instance of {} with attributes {}'
            .format(model_cls, field_data)
        )
        raise
    return instance


def _resolve_foreign_keys(model_cls, record):
    """Retrieve and link instances of models referred to by FK

    This is the one step that imposes a dependency order to the data load.
    The instance that is referred to must already exist.
    """
    new_record = {}
    for field in record.keys():
        field_data = record[field]
        model_field = model_cls._meta.get_field(field)

        if model_field.get_internal_type() == "ForeignKey":
            new_record[field] = _retrieve_existing_model_instance(
                model_field.rel.to, field_data)
        else:
            new_record[field] = field_data

    return new_record


def _instantiate_single_record(model, unique_fields, record):
    """Create unsaved model instances, ready to be sent to bulk_create"""
    app, model_name = model.split('.', 1)  # split only once
    model_cls = get_model(app, model_name)

    if unique_fields:
        unique_dict = {}
        for field in unique_fields:
            model_field = model_cls._meta.get_field(field)
            field_data = record[field]
            if model_field.get_internal_type() == "ForeignKey":
                field_data = field_data.copy()
                instance = _retrieve_existing_model_instance(
                    model_field.rel.to, field_data)
                unique_dict[field] = instance
            else:
                unique_dict[field] = field_data

        try:
            instance = model_cls.objects.get(**unique_dict)
            return model_cls, None  # Must test for None in calling code
        except model_cls.DoesNotExist:
            try:
                normalized_record = _resolve_foreign_keys(model_cls, record)
                instance = model_cls(**normalized_record)

                # Do not allow SequenceField fields to go to the DB null
                # bulk_create will not call our custom save()
                for field in instance._meta.fields:
                    if (
                        isinstance(field, SequenceField)
                        and not getattr(instance, field.name)
                        and hasattr(instance, 'generate_next_code_sequence')
                            ):
                        setattr(
                            instance,
                            field.name,
                            instance.generate_next_code_sequence()
                        )

                return model_cls, instance
            except Exception as e:  # Don't panic, we will be re-raising
                LOGGER.error(
                    '"{}" when instantiating a record of "{}" with unique '
                    'fields "{}" and data "{}"'
                    .format(e, model, unique_fields, record)
                )
                raise
    else:
        LOGGER.error('Data file error; unique fields not specified')


def _process_model_spec(model_spec):
    """For each model spec, instantiate but do not save ( bulk save later )"""
    model = model_spec['model']
    unique_fields = model_spec.get('unique_fields', [])
    records = model_spec['records']

    # The first version of this function used some fancy functional techniques
    # ( partials / currying ); we go back to a simpler, more deterministic way
    unsaved_instances = defaultdict(list)
    for record in records:
        model_cls, unsaved_obj = _instantiate_single_record(
            model, unique_fields, record)
        if unsaved_obj:  # For existing instances, obj is set to `None`
            unsaved_instances[model_cls].append(unsaved_obj)

    for model_cls, instances in unsaved_instances.iteritems():
        with transaction.atomic():
            model_cls.objects.bulk_create(instances)
            LOGGER.debug(
                'Created {} instances of {}'.format(len(instances), model_cls))


def process_json_file(filename):
    """The entry point - loops through data files and loads each in"""
    LOGGER.debug('Processing {}'.format(filename))
    with open(filename) as f:
        model_specs = json.load(f)
        map(_process_model_spec, model_specs)
