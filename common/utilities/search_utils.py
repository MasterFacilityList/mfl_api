import pydoc

from django.conf import settings
from django.apps import apps
import requests

ELASTIC_URL = settings.SEARCH.get('ELASTIC_URL')


class ElasticAPI(object):
    def setup_index(self, index_name):
        url = ELASTIC_URL + index_name
        result = requests.put(url)
        return result

    def get_index(self, index_name):
        url = ELASTIC_URL + index_name
        result = requests.get(url)
        return result

    def delete_index(self, index_name):
        url = ELASTIC_URL + index_name
        result = requests.delete(url)
        return result

    def index_instance(self, index_name, instane_data):
        instance_type = instane_data.get('instance_type')
        instance_id = instane_data.get('instance_id')
        url = ELASTIC_URL + index_name + instance_type + instance_id
        result = requests.put(url, instane_data)
        return result


def serialize_model(obj):
    """
    Locates a models serializer and uses it to serializer a model instane
    This allows us to search a document through all its important components.
    If a attribute of model is important enough to appear in the serializer,
    it means that the models should also be searched though that attribute
    as well. This will take care for all the child models of a model if
    they have been inlined in the serializer.

    For this to work a model's serializer name should follow this convention
    '<model_name>Serializer'

    Only apps in local apps will be indexed.
    """
    app_label = obj._meta.app_label
    serializer_path = "{}{}{}{}".format(
        app_label, ".serializers.", obj.__class__.__name__, 'Serializer')
    serializer_cls = pydoc.locate(serializer_path)
    serialized_data = serializer_cls(obj).data
    return {
        "data": serialized_data,
        "index_type": obj.__class__.__name__.lower(),
        "id": str(obj.id)
    }
