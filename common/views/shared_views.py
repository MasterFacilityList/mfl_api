from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse as django_reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from ..metadata import CustomMetadata


# The current dict is hand rolled; a future version could be generated
MODEL_VIEW_DICT = {
    'contact_types': {
        'list_url': 'api:common:contact_types_list',
        'detail_url': 'api:common:contact_type_detail'
    },
    'user_residence': {
        'list_url': 'api:common:user_wards_list',
        'detail_url': 'api:common:user_ward_detail'
    },
    'user_contacts': {
        'list_url': 'api:common:user_contacts_list',
        'detail_url': 'api:common:user_contact_detail'
    },
    'contacts': {
        'list_url': 'api:common:contacts_list',
        'detail_url': 'api:common:contact_detail'
    },
    'counties': {
        'list_url': 'api:common:counties_list',
        'detail_url': 'api:common:county_detail'
    },
    'user_counties': {
        'list_url': 'api:common:user_counties_list',
        'detail_url': 'api:common:user_county_detail'
    },
    'wards': {
        'list_url': 'api:common:wards_list',
        'detail_url': 'api:common:ward_detail'
    },
    'towns': {
        'list_url': 'api:common:towns_list',
        'detail_url': 'api:common:town_detail'
    },
    'constituencies': {
        'list_url': 'api:common:constituencies_list',
        'detail_url': 'api:common:constituency_detail'
    },
    'users': {
        'list_url': 'api:users:users_list',
        'detail_url': 'api:users:user_detail'
    },
    'facility_units': {
        'list_url': 'api:facilities:facility_units_list',
        'detail_url': 'api:facilities:facility_unit_detail'
    },
    'regulating_bodies': {
        'list_url': 'api:facilities:regulating_bodies_list',
        'detail_url': 'api:facilities:regulating_body_detail'
    },
    'facility_types': {
        'list_url': 'api:facilities:facility_types_list',
        'detail_url': 'api:facilities:facility_type_detail'
    },
    'facility_status': {
        'list_url': 'api:facilities:facility_status_list',
        'detail_url': 'api:facilities:facility_status_detail'
    },
    'facilities': {
        'list_url': 'api:facilities:facility_list',
        'detail_url': 'api:facilities:facility_detail'
    },
    'officer_in_charge_contacts': {
        'list_url': 'api:facilities:officer_incharge_contacts_list',
        'detail_url': 'api:facilities:officer_incharge_detail'
    },
    'job_titles': {
        'list_url': 'api:facilities:job_titles_list',
        'detail_url': 'api:facilities:job_title_detail'
    },
    'geo_code_sources': {
        'list_url': 'api:facilities:geo_code_sources_list',
        'detail_url': 'api:facilities:geo_code_source_detail'
    },
    'facility_regulation_status': {
        'list_url': 'api:facilities:facility_regulation_status_list',
        'detail_url': 'api:facilities:facility_regulation_status_detail'
    },
    'regulation_status': {
        'list_url': 'api:facilities:regulation_status_list',
        'detail_url': 'api:facilities:regulation_status_detail'
    },
    'geo_code_methods': {
        'list_url': 'api:facilities:geo_code_methods_list',
        'detail_url': 'api:facilities:geo_code_method_detail'
    },
    'officers_in_charge': {
        'list_url': 'api:facilities:officers_incharge_list',
        'detail_url': 'api:facilities:officer_incharge_detail'
    },
    'service_categories': {
        'list_url': 'api:facilities:service_categories_list',
        'detail_url': 'api:facilities:service_category_detail'
    },
    'owner_types': {
        'list_url': 'api:facilities:facility_list',
        'detail_url': 'api:facilities:facility_detail'
    },
    'owners': {
        'list_url': 'api:facilities:owners_list',
        'detail_url': 'api:facilities:owner_detail'
    },
    'services': {
        'list_url': 'api:facilities:services_list',
        'detail_url': 'api:facilities:service_detail'
    },
    'facility_services': {
        'list_url': 'api:facilities:facility_services_list',
        'detail_url': 'api:facilities:facility_service_detail'
    },
    'facility_gis': {
        'list_url': 'api:facilities:facility_gis_list',
        'detail_url': 'api:facilities:facility_gis_detail'
    }
}
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

# TODO Introspect and reverse all list URLs
#    ( should be easy to introspect views from all apps )
# TODO Retrieve metadata for each of those URLs and inline it for lists
# TODO Retrieve metadata and inline it for detail URLs
# ( what can a detail URL do? )
# TODO Add audit URls for every model; override render?
