import uuid

from collections import defaultdict, OrderedDict

from django.conf import settings
from django.apps import apps
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse as django_reverse

from rest_framework.reverse import reverse

from ..metadata import CustomMetadata

METADATA_CLASS = CustomMetadata()


def _create_model_view_dict():
    """
    This reads the models in settings.LOCAL_APPS and "generates" ( more like
    imagines ) the applicable detail and list URLs.

    It is a tough task master; it assumes that the URLs are named following a
    strict convention:

        * detail views -> 'api:<app_name>:<applicable_model_verbose_name>'
        * list views -> 'api:<app_name>:<applicable_model_verbose_name_plural>'

    It will **blow up** under two circumstances:

        * you have a concrete model that does not have views and URLs
        ( your bad, a spectacular test failure will let you know about it )
        * you violated naming conventions
        ( helpers can be supplied to make that easy )

    A future version of this might introspect the registered views / URLs and
    create the metadata and API root listing in a more forgiving manner. At
    the time of writing this, the author was too pressed for time.
    """
    return_dict = defaultdict(dict)
    for app_name in settings.LOCAL_APPS:  # We must keep our apps in LOCAL_APPS
        app_models = apps.get_app_config(app_name).get_models()

        for app_model in app_models:
            return_dict[app_model] = {
                'list_url': 'api:{}:{}_list'.format(
                    app_name,
                    str(app_model._meta.verbose_name_plural).replace(' ', '_')
                ),
                'detail_url': 'api:{}:{}_detail'.format(
                    app_name,
                    app_model._meta.verbose_name.replace(' ', '_')
                )
            }

    # This must stay as the sole exit path
    return return_dict

# When things are flaming out, examine this
MODEL_VIEW_DICT = _create_model_view_dict()


def _reverse(request, url_name):
    """Extracted for space saving reasons and nothing more"""
    return reverse(url_name, request=request)


def _resolve_list_metadata(request, url_name):
    url_path = django_reverse(url_name)
    view = resolve(url_path).func.cls()
    view.initial(request)
    return METADATA_CLASS.determine_metadata(request, view)


def _get_metadata_from_detail_url(url_name, request):
    pk = str(uuid.uuid4())  # Random PK, likely non-existent; does not matter
    url_path = django_reverse(url_name, kwargs={'pk': pk})
    view = resolve(url_path).func.cls(kwargs={'pk': pk})
    view.initial(request, kwargs={'pk': pk})
    return METADATA_CLASS.determine_metadata(request, view)


def _resolve_detail_metadata(request, url_name, model_cls):
    """I am not proud of this"""
    metadata = _get_metadata_from_detail_url(url_name, request)
    return metadata


def _lookup_metadata(url_name_dict, request, model_cls, view):
    """
    This is what composes the final payload that goes to the client
    """
    # Using an ordered dict to control the presentation
    metadata_dict = OrderedDict()
    metadata_dict['list_endpoint'] = \
        _reverse(request, url_name_dict['list_url'])
    metadata_dict['list_metadata'] = \
        _resolve_list_metadata(request, url_name_dict['list_url'])
    metadata_dict['detail_metadata'] = \
        _resolve_detail_metadata(
            request, url_name_dict['detail_url'], model_cls)
    return metadata_dict
