from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse as django_reverse
from django.conf import settings
from collections import defaultdict
from django.apps import apps
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from ..metadata import CustomMetadata


# TODO Get the list of all models and generate URLs from it; share the dict
# TODO Fix metadata with no object ( detail view )

def _create_model_view_dict():
    return_dict = defaultdict(dict)
    for app_name in settings.LOCAL_APPS:  # We must keep our apps in LOCAL_APPS
        app_models = apps.get_app_config(app_name).get_models()

        for app_model in app_models:
            return_dict[app_model._meta.verbose_name] = {
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


MODEL_VIEW_DICT = _create_model_view_dict()
METADATA_CLASS = CustomMetadata()


def _reverse(request, url_name):
    return reverse(
        url_name,
        request=request
    )


def _resolve_list_metadata(request, url_name):
    url_path = django_reverse(url_name)
    view = resolve(url_path).func.cls()
    view.initial(request)
    return METADATA_CLASS.determine_metadata(request, view)


def _resolve_detail_metadata(request, url_name):
    url_path = django_reverse(url_name, kwargs={'pk': None})
    view = resolve(url_path).func.cls(kwargs={'pk': None})
    view.initial(request)
    return METADATA_CLASS.determine_metadata(request, view)


def _lookup_metadata(url_name_dict, request):
    return {
        'list_endpoint':
            _reverse(request, url_name_dict['list_url']),
        'list_metadata':
            _resolve_list_metadata(
                request,
                url_name_dict['list_url']
            ),
        'detail_metadata':
            _resolve_detail_metadata(
                request,
                url_name_dict['detail_url']
            )
    }


class APIRoot(APIView):
    """
    This view serves as the entry point to the entire API
    """

    def get(self, request, format=None):
        return Response({
            model_type_name: _lookup_metadata(url_name_dict, request)
            for model_type_name, url_name_dict in MODEL_VIEW_DICT.iteritems()
        })
