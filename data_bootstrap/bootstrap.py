import json
import logging

from functools import partial
from django.db.models import get_model


LOGGER = logging.getLogger(__name__)


def get_model_cls(model):
    app, model_name = model.split('.', 1)  # split only once
    return get_model(app, model_name)


def resolve_foreign_key(model_cls, field_data):
    # to prevent any modifications making their way back to
    # the original dict
    assert isinstance(field_data, dict)
    try:
        instance = model_cls.objects.get(**field_data)
    except:
        LOGGER.error(
            'Unable to get an instance of {} with {}'
            .format(model_cls, field_data)
        )
        raise
    return instance


def resolve_foreign_keys(model_cls, record):
    new_record = {}
    for field in record.keys():
        field_data = record[field]
        model_field = model_cls._meta.get_field(field)
        if model_field.get_internal_type() == "ForeignKey":
            new_record[field] = resolve_foreign_key(
                model_field.rel.to, field_data)
        else:
            new_record[field] = field_data

    return new_record


def process_record(model, unique_fields, record):
    model_cls = get_model_cls(model)

    if unique_fields:
        unique_dict = {}
        for field in unique_fields:
            model_field = model_cls._meta.get_field(field)
            field_data = record[field]
            if model_field.get_internal_type() == "ForeignKey":
                field_data = field_data.copy()
                instance = resolve_foreign_key(
                    model_field.rel.to, field_data)
                unique_dict[field] = instance
            else:
                unique_dict[field] = field_data

        try:
            model_cls.objects.get(**unique_dict)
        except model_cls.DoesNotExist:
            pass
        else:
            # record is already in the database so don't add
            return

    normalized_record = resolve_foreign_keys(model_cls, record)
    model_cls.objects.create(**normalized_record)


def process_model_spec(model_spec):
    model = model_spec['model']
    unique_fields = model_spec.get('unique_fields', [])
    records = model_spec['records']

    temp_func = partial(process_record, model, unique_fields)
    map(temp_func, records)


def process_data_list(data):
    map(process_model_spec, data)


def process_json_file(filename):
    with open(filename) as f:
        data = f.read()
        json_data = json.loads(data)
        process_data_list(json_data)
