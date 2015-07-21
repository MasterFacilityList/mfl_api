import logging
import reversion

from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin

LOGGER = logging.getLogger(__name__)


class AuditableDetailViewMixin(RetrieveModelMixin):
    """
    A very thin extension of the default `RetrieveModelMixin` that adds audit.

    As at Django REST Framework 3.1, `RetrieveModelMixin` looks like this:

        ```
        class RetrieveModelMixin(object):
            '''
            Retrieve a model instance.
            '''
            def retrieve(self, request, *args, **kwargs):
                instance = self.get_object()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
        ```

    Our variant is not very different...all it does is to look for an
    `include_audit` GET param ( boolean ) in the request. If it is found,
    we include that model instance's audit information in the returned
    representation.

    We are counting on the fact that this API operates only on a single
    *instance* AND the fact that audit data is optional ( opt-in ); hence
    the lack of pagination of the revisions.

    Reconstruction will be left to the client / consumer of this API.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        if str(request.query_params.get('include_audit', None)).lower() in \
                ['true', 'yes', 'y', '1', 't']:
            data["revisions"] = [
                version.field_dict
                for version in reversion.get_for_object(instance)
            ]

        return Response(data)


class APIRoot(APIView):
    """
    This view serves as the entry point to the entire API.

    # Exploring the API
    There are two ways to explore this API:

     * the [Swagger](http://swagger.io/)
     [**sandbox** ( click here )](/api/explore/#!/api)
     * the browsable API
    # Authentication
    Anonymous users have **read only** access to *most* ( not all ) views.
    If you want to try out the `POST`, `PUT`, `PATCH` and `DELETE` actions,
    you will need to log in using the link on the top right corner.

    For the experimental sandbox, you can get suitable credentials from
    [the documentation](http://mfl-api.readthedocs.org/en/latest/). For a live
    instance, you need to request for access from the administrators.
    """
    def get(self, request, format=None):
        return Response()


def root_redirect_view(request):
    return redirect('api:root_listing', permanent=True)
