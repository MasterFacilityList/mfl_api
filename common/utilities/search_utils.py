import pydoc
import json
import uuid
import requests


from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


ELASTIC_URL = settings.SEARCH.get('ELASTIC_URL')
INDEX_NAME = settings.SEARCH.get('INDEX_NAME')


def default(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)


class ElasticAPI(object):
    def setup_index(self, index_name=INDEX_NAME):
        url = ELASTIC_URL + index_name
        result = requests.put(url)
        return result

    def get_index(self, index_name):
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
        url = "{}{}{}{}{}{}{}".format(
            ELASTIC_URL, index_name, "/", instance_type, "/",
            '_search?q=', query)
        result = requests.get(url)

        return result


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

    serialized_data = serializer_cls(obj).data

    serialized_data = json.dumps(serialized_data, default=default)
    return {
        "data": serialized_data,
        "instance_type": obj.__class__.__name__.lower(),
        "instance_id": str(obj.id)
    }


def index_instance(obj, index_name=INDEX_NAME):
    elastic_api = ElasticAPI()
    data = serialize_model(obj)
    return elastic_api.index_document(index_name, data)


@receiver(post_save)
def index_on_save(sender, instance, **kwargs):
    """
    Listen for save signals and index the insances being created.
    """
    app_label = instance._meta.app_label
    index_in_realtime = settings.SEARCH.get("REALTIME_INDEX")
    if app_label in settings.LOCAL_APPS:
        index_instance(instance) if index_in_realtime else None
