from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse as django_reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from ..metadata import CustomMetadata


# The current dict is hand rolled; a future version could be generated
MODEL_VIEW_DICT = {
    'contact_types': {
        'list_url_name': 'api:common:contact_types_list'
    },
    'user_residence': {
        'list_url_name': 'api:common:user_wards_list'
    },
    'user_contacts': {
        'list_url_name': 'api:common:user_contacts_list'
    },
    'contacts': {
        'list_url_name': 'api:common:user_contacts_list'
    },
    'counties': {
        'list_url_name': 'api:common:counties_list'
    },
    'user_counties': {
        'list_url_name': 'api:common:user_counties_list'
    },
    'wards': {
        'list_url_name': 'api:common:wards_list'
    },
    'towns': {
        'list_url_name': 'api:common:towns_list'
    },
    'constituencies': {
        'list_url_name': 'api:common:constituencies_list'
    },
    'users': {
        'list_url_name': 'api:users:users_list'
    },
    'facility_units': {
        'list_url_name': 'api:facilities:facility_units_list'
    },
    'regulating_bodies': {
        'list_url_name': 'api:facilities:regulating_bodies_list'
    },
    'facility_types': {
        'list_url_name': 'api:facilities:facility_types_list'
    },
    'facility_status': {
        'list_url_name': 'api:facilities:facility_status_list'
    },
    'facilities': {
        'list_url_name': 'api:facilities:facility_list'
    },
    'officer_in_charge_contacts': {
        'list_url_name': 'api:facilities:officer_incharge_contacts_list'
    },
    'job_titles': {
        'list_url_name': 'api:facilities:job_titles_list'
    },
    'geo_code_sources': {
        'list_url_name': 'api:facilities:geo_code_sources_list'
    },
    'facility_regulation_status': {
        'list_url_name': 'api:facilities:facility_regulation_status_list'
    },
    'regulation_status': {
        'list_url_name': 'api:facilities:regulation_status_list'
    },
    'geo_code_methods': {
        'list_url_name': 'api:facilities:geo_code_methods_list'
    },
    'officers_in_charge': {
        'list_url_name': 'api:facilities:officers_incharge_list'
    },
    'service_categories': {
        'list_url_name': 'api:facilities:service_categories_list'
    },
    'owner_types': {
        'list_url_name': 'api:facilities:facility_list'
    },
    'owners': {
        'list_url_name': 'api:facilities:owners_list'
    },
    'services': {
        'list_url_name': 'api:facilities:services_list'
    },
    'contacts': {
        'list_url_name': 'api:common:contacts_list'
    },
    'facility_services': {
        'list_url_name': 'api:facilities:facility_services_list'
    },
    'facility_gis': {
        'list_url_name': 'api:facilities:facility_gis_list'
    }
}
METADATA_CLASS = CustomMetadata()


def _reverse(request, url_name):
    return reverse(
        url_name,
        request=request
    )


def _resolve_metadata(request, url_name):
    url_path = django_reverse(url_name)
    view = resolve(url_path).func.cls()
    view.initial(request)
    return METADATA_CLASS.determine_metadata(request, view)


def _lookup_metadata(url_name_dict, request):
    return {
        'list_endpoint':
            _reverse(request, url_name_dict['list_url_name']),
        'list_metadata':
            _resolve_metadata(
                request,
                url_name_dict['list_url_name']
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

# TODO Introspect and reverse all list URLs
#    ( should be easy to introspect views from all apps )
# TODO Retrieve metadata for each of those URLs and inline it for lists
# TODO Retrieve metadata and inline it for detail URLs
# ( what can a detail URL do? )
# TODO Add audit URls for every model; override render?
