import pydoc
import json
import uuid
import requests
import logging

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import get_app, get_models
from common.models import ErrorQueue
from celery import shared_task

from .index_settings import INDEX_SETTINGS

ELASTIC_URL = settings.SEARCH.get('ELASTIC_URL')
AUTO_COMPLETE_MODELS = settings.SEARCH.get('AUTOCOMPLETE_MODEL_FIELDS')
INDEX_NAME = settings.SEARCH.get('INDEX_NAME')
SEARCH_RESULT_SIZE = settings.SEARCH.get('SEARCH_RESULT_SIZE')
SEARCH_FIELDS = settings.SEARCH.get('FULL_TEXT_SEARCH_FIELDS')
LOGGER = logging.getLogger(__name__)


def default(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)


class ElasticAPI(object):

    @property
    def _is_on(self):
        url = ELASTIC_URL
        try:
            requests.get(url)
            return True
        except requests.exceptions.ConnectionError:
            return False

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

    def get_search_fields(self, model_name):
        for field in SEARCH_FIELDS.get("models"):
            if field.get("name") == model_name:
                return field.get("fields")

    def search_document(self, index_name, instance_type, query):
        document_type = instance_type.__name__.lower()
        url = "{}{}/{}/_search".format(
            ELASTIC_URL, index_name, document_type)
        search_fields = self.get_search_fields(document_type)
        fields = search_fields if self.get_search_fields(document_type) else \
            ["_all"]
        query_dsl = None

        # This allows one to search for something either using an exact value
        # like code e.g 1000
        # or query DSL e.g {
        #    "query": query_string:{
        #               'default_field':'field_name", quuery:'search term'}}
        # or just a string e.g 'nairobi hospital'

        try:
            json.loads(query)
            query_dsl = query
        except (ValueError, TypeError):
            LOGGER.info("The user did not use query DSL")

        data = {
            "from": 0,
            "size": SEARCH_RESULT_SIZE,
            "query": {
                "fuzzy_like_this": {
                    "fields": fields,
                    "like_text": query,
                    "max_query_terms": 12
                }
            }
        }

        data = json.dumps(data)
        if query_dsl:
            result = requests.post(url, query_dsl)
        else:
            result = requests.post(url, data)

        return result

    def search_auto_complete_document(self, index_name, instance_type, query):
        search_fields = ["name"]
        document_type = instance_type.__name__.lower()
        for model_config in AUTO_COMPLETE_MODELS:
            for model in model_config.get('models'):
                if model.get('name').lower() == document_type:
                    search_fields = model.get('fields')
                    break

        url = "{}{}/{}/_search".format(
            ELASTIC_URL, index_name, document_type)
        data = {
            "from": 0,
            "size": SEARCH_RESULT_SIZE,
            "query": {
                "query_string": {
                    "fields": search_fields,
                    "query": query,
                    "analyzer": "autocomplete"
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


@shared_task(name='Update_the_search_index')
def index_instance(app_label, model_name, instance_id, index_name=INDEX_NAME):
    indexed = False
    elastic_api = ElasticAPI()
    obj_path = "{0}.models.{1}".format(app_label, model_name)
    obj = pydoc.locate(obj_path).objects.get(id=instance_id)
    if not elastic_api._is_on:
        ErrorQueue.objects.get_or_create(
            object_pk=str(obj.pk),
            app_label=obj._meta.app_label,
            model_name=obj.__class__.__name__,
            except_message="Elastic Search is not running",
            error_type="SEARCH_INDEXING_ERROR"
        )
        return indexed

    if confirm_model_is_indexable(obj.__class__):
        data = serialize_model(obj)
        if data:
            elastic_api.index_document(index_name, data)
            LOGGER.info("Indexed {0}".format(data))
            indexed = True
        else:
            LOGGER.info(
                "something unexpected occurred when indexing {} - {}"
                .format(model_name, instance_id)
            )
    else:
        LOGGER.info(
            "Instance of model {} skipped for indexing as it should not be"
            " indexed".format(obj.__class__))
    return indexed


@receiver(post_save)
def index_on_save(sender, instance, **kwargs):
    """
    Listen for save signals and index the instances being created.
    """
    if sender == ErrorQueue:
        return
    app_label = instance._meta.app_label
    index_in_realtime = settings.SEARCH.get("REALTIME_INDEX")
    model_name = sender.__name__
    instance_id = str(instance.id) if hasattr(instance, 'id') else None

    index_instance.delay(app_label, model_name, instance_id) if app_label \
        in settings.LOCAL_APPS and index_in_realtime else None
