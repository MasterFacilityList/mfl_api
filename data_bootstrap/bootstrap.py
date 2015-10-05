import json
import logging
import os

from collections import defaultdict
from django.apps import apps
from django.db import transaction
from django.db.utils import ProgrammingError
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist

from common.fields import SequenceField

LOGGER = logging.getLogger(__name__)


def _retrieve_existing_model_instance(model_cls, field_data):
    """RETRIEVE an existing model instance ( mainly used to resolve FKs )"""
    # to prevent any modifications making their way back to
    # the original dict
    assert isinstance(field_data, dict)
    try:
        instance = model_cls.objects.get(**field_data)
    except (ProgrammingError, ObjectDoesNotExist):

        keys = field_data.keys()
        for key in keys:
            value = field_data[key]
            if isinstance(value, dict):
                fk_model = model_cls._meta.get_field(key).rel.to
                fk_instance = fk_model.objects.get(**value)
                field_data[key] = fk_instance
            else:
                # the field is not a foreign key hence no need to upate
                # the dict with a model instance
                pass

        instance = model_cls.objects.get(**field_data)

    return instance


def _resolve_foreign_keys_and_coordinates(model_cls, record):
    """Retrieve and link instances of models referred to by FK

    Also resolve any GIS ( geojson ) coordinates embedded in the data.

    This is the one step that imposes a dependency order to the data load.
    The instance that is referred to must already exist.
    """
    new_record = {}
    for field in record.keys():
        field_data = record[field]
        model_field = model_cls._meta.get_field(field)

        if model_field.get_internal_type() in [
                "ForeignKey", "OneToOneField"]:
            new_record[field] = _retrieve_existing_model_instance(
                model_field.rel.to, field_data)
        elif model_field.get_internal_type() == "PointField":
            new_record[field] = Point(json.loads(field_data)["coordinates"])
        else:
            new_record[field] = field_data

    return new_record


def _instantiate_single_record(model, unique_fields, record):
    """Create unsaved model instances, ready to be sent to bulk_create"""
    assert isinstance(model, str) or isinstance(model, unicode)
    assert isinstance(unique_fields, list)
    assert isinstance(record, dict)

    app, model_name = model.split('.', 1)  # split only once
    model_cls = apps.get_model(app_label=app, model_name=model_name)

    if unique_fields:
        unique_dict = {}
        for field in unique_fields:
            model_field = model_cls._meta.get_field(field)
            field_data = record[field]
            if model_field.get_internal_type() in [
                    "ForeignKey", "OneToOneField"]:
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
                normalized_record = _resolve_foreign_keys_and_coordinates(model_cls, record)  # NOQA
                assert isinstance(normalized_record, dict)
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
        except model_cls.MultipleObjectsReturned as ex:
            LOGGER.error(
                'Data bug ( non unique ): "{}". '
                'It relates to record "{}" of model "{}", unique fields "{}".'
                .format(ex, record, model, unique_fields)
            )
            return None, None  # Calling code should be able to handle this
    else:
        LOGGER.error('Data file error; unique fields not specified')


def _process_model_spec(model_spec):
    """For each model spec, instantiate but do not save ( bulk save later )"""
    model = model_spec['model']
    unique_fields = model_spec['unique_fields']

    records = model_spec['records']

    assert isinstance(model, str) or isinstance(model, unicode)
    assert isinstance(unique_fields, list)
    assert isinstance(records, list)
    assert len(records) > 0

    # The first version of this function used some fancy functional techniques
    # ( partials / currying ); we go back to a simpler, more deterministic way
    unsaved_instances = defaultdict(list)
    for record in records:
        assert isinstance(record, dict)
        try:
            model_cls, unsaved_obj = _instantiate_single_record(
                model, unique_fields, record
            )
        except Exception as ex:  # Broad catch, reraised after debug logging
            LOGGER.error('{} when working on {}'.format(ex, record))
            raise

        if unsaved_obj:  # For existing instances, obj is set to `None`
            unsaved_instances[model_cls].append(unsaved_obj)

    for model_cls, instances in unsaved_instances.iteritems():
        with transaction.atomic():
            model_cls.objects.bulk_create(instances)
            LOGGER.info(
                'Created {} instances of {}'.format(len(instances), model_cls))


def process_json_file(filename):
    """The entry point - loops through data files and loads each in"""
    assert isinstance(filename, str)
    if os.path.isdir(filename):
        LOGGER.info("Filename points to a directory")
        return
    else:
        LOGGER.info('Processing {}'.format(filename))

        with open(filename) as f:
            model_specs = json.load(f)
            assert isinstance(model_specs, list)
            assert len(model_specs) > 0

            for model_spec in model_specs:
                try:
                    _process_model_spec(model_spec)
                except Exception as ex:  # Broad catch to allow debug messages
                    import traceback
                    traceback.print_exc()
                    LOGGER.error(
                        '{} when processing {:.1000}'.format(ex, model_spec))
