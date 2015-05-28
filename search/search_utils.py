import pydoc
import json
import uuid
import requests
import logging

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import get_app, get_models

from .index_settings import INDEX_SETTINGS

ELASTIC_URL = settings.SEARCH.get('ELASTIC_URL')
INDEX_NAME = settings.SEARCH.get('INDEX_NAME')
LOGGER = logging.getLogger(__name__)


def default(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)


class ElasticAPI(object):
    def setup_index(self, index_name=INDEX_NAME):
        url = ELASTIC_URL + index_name
        mfl_settings = json.dumps(INDEX_SETTINGS)
        result = requests.put(url, data=mfl_settings)
        return result

    def get_index(self, index_name=INDEX_NAME):
        url = ELASTIC_URL + index_name
        result = requests.get(url)
        return result

    def delete_index(self, index_name=INDEX_NAME):
        url = ELASTIC_URL + index_name
        result = requests.delete(url)
        return result

    def index_document(self, index_name, instance_data):
        instance_type = instance_data.get('instance_type')
        instance_id = instance_data.get('instance_id')
        data = instance_data.get('data')
        url = "{}{}{}{}{}{}".format(
            ELASTIC_URL, index_name, "/", instance_type, "/", instance_id)
        result = requests.put(url, data)
        return result

    def remove_document(self, index_name, document_type, document_id):
        url = "{}{}{}{}{}{}".format(
            ELASTIC_URL, index_name, "/", document_type, "/", document_id)
        result = requests.delete(url)
        return result

    def search_document(self, index_name, instance_type, query):
        document_type = instance_type.__name__.lower()
        url = "{}{}/{}/_search".format(
            ELASTIC_URL, index_name, document_type)
        data = {
            "query": {
                "query_string": {
                    "query": query
                }
            }
        }
        data = json.dumps(data)
        result = requests.post(url, data)

        return result


def confirm_model_is_indexable(model):
        non_indexable_models = settings.SEARCH.get('NON_INDEXABLE_MODELS')
        non_indexable_models_classes = []
        non_indexable_models_names = []
        for app_model in non_indexable_models:
            app_name, cls_name = app_model.split('.')
            non_indexable_models_names.append(cls_name)
            app = get_app(app_name)
            app_models = get_models(app)

            for model_cls in app_models:
                if model_cls.__name__ in non_indexable_models_names:
                    non_indexable_models_classes.append(model_cls)
        non_indexable_models_classes = list(set(non_indexable_models_classes))
        return True if model not in non_indexable_models_classes else False


def serialize_model(obj):
    """
    Locates a models serializer and uses it to serialize a model instance
    This allows us to search a document through all its important components.
    If a attribute of model is important enough to make it to the model
    serializer,
    it means that the models should also be searched though that attribute
    as well. This will take care for all the child models of a model if
    they have been inlined in the serializer.

    For this to work, a model's serializer name has to follow this convention
    '<model_name>Serializer' Failing to do so the function will cause the
    function throw a TypeError exception.
    Only apps in local apps will be indexed.
    """
    app_label = obj._meta.app_label
    serializer_path = "{}{}{}{}".format(
        app_label, ".serializers.", obj.__class__.__name__, 'Serializer')
    serializer_cls = pydoc.locate(serializer_path)
    if not serializer_cls:
        LOGGER.info("Unable to locate a serializer for model {}".format(
            obj.__class__))
    else:

        serialized_data = serializer_cls(obj).data

        serialized_data = json.dumps(serialized_data, default=default)
        return {
            "data": serialized_data,
            "instance_type": obj.__class__.__name__.lower(),
            "instance_id": str(obj.id)
        }


def index_instance(obj, index_name=INDEX_NAME):
    elastic_api = ElasticAPI()
    if confirm_model_is_indexable(obj.__class__):
        data = serialize_model(obj)
        return elastic_api.index_document(index_name, data)
    else:
        LOGGER.info(
            "Instance of model {} skipped for indexing as it should not be"
            " indexed".format(obj.__class__))


@receiver(post_save)
def index_on_save(sender, instance, **kwargs):
    """
    Listen for save signals and index the instances being created.
    """
    app_label = instance._meta.app_label
    index_in_realtime = settings.SEARCH.get("REALTIME_INDEX")
    if app_label in settings.LOCAL_APPS:
        index_instance(instance) if index_in_realtime else None
