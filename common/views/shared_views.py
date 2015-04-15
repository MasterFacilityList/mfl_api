from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse


class APIRoot(APIView):

    def get(self, request, format=None):
        return Response({
            'counties': reverse(
                'api:common:counties_list',
                request=request,
                format=format
            ),
            'users': reverse(
                'api:users:users_list', request=request, format=format
            ),
            'facilities': reverse(
                'api:facilities:facility_list',
                request=request,
                format=format
            ),
            'contacts': reverse(
                'api:common:contacts_list',
                request=request,
                format=format
            ),
            'contact_types': reverse(
                'api:common:contact_types_list',
                request=request,
                format=format
            ),
            'wards': reverse(
                'api:common:wards_list',
                request=request,
                format=format
            ),
            'constituencies': reverse(
                'api:common:constituencies_list',
                request=request,
                format=format
            ),
            'owners': reverse(
                'api:facilities:owners_list',
                request=request,
                format=format
            ),
            'owner_types': reverse(
                'api:facilities:facility_list',
                request=request,
                format=format
            ),
            'services': reverse(
                'api:facilities:services_list',
                request=request,
                format=format
            )
        })

# TODO Do the root API view in class based view style
# TODO Introspect and reverse all list URLs
#    ( should be easy to introspect views from all apps )
# TODO Retrieve metadata for each of those URLs and inline it for lists
# TODO Retrieve metadata and inline it for detail URLs
# ( what can a detail URL do? )
# TODO Add audit URls for every model; override render?
