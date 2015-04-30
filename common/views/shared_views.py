import logging
import reversion

from collections import OrderedDict
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from ..utilities.metadata_helpers import MODEL_VIEW_DICT, _lookup_metadata

from ..metadata import CustomMetadata

METADATA_CLASS = CustomMetadata()
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
    This view serves as the entry point to the entire API. It also hosts all
    the metadata.

    # Exploring the API
    There are two ways to explore this API:

     * the [Swagger](http://swagger.io/)
     [**sandbox** ( click here )](/api/explore/#!/api)
     * the browsable API - available through clickable links in the metadata
     listing below

    # Authentication
    Anonymous users have **read only** access to *most* ( not all ) views.
    If you want to try out the `POST`, `PUT`, `PATCH` and `DELETE` actions,
    you will need to log in using the link on the top right corner.

    For the experimental sandbox, you can get suitable credentials from
    [the documentation](http://mfl-api.readthedocs.org/en/latest/). For a live
    instance, you need to request for access from the administrators.

    # Understanding the metadata listing
    The metadata listing can at first appear to be intimidating, given that it
    carries metadata for all API views.

    It has a simple structure it is a dictionary ( map ) of dictionaries.
    Each entry in the dictionary follows the following scheme:

        "<1: Resource Name>": {
            "list_endpoint": "<2: List URL>",
            "list_metadata": "<3: List Metadata Payload>",
            "detail_metadata": <4: Detail Metadata Payload>"
        }

    ## 1: Resource Name
    This is the name of a "thing" e.g `county`.

    ## 2: List URL
    This is a fully qualified URL to a view that **lists** instances of the
    resource in question. In this server, list views support `GET`
    ( retrieval of many resources at once ) and `POST` ( creation of new
    resources ).

    All the links shown in the browseable API are clickable.

    For example: `http://localhost:8000/api/common/counties/` .

    ## 3: List Metadata Payload
    This payload takes the following form:

        {
            "name": "<Name of the list view>",
            "description": "<A human readable description>",
            "renders": "<a. Output formats for the list API>",
            "parses": "<b. Input formats for the list API>",
            "actions": "<c. Actions supported by the list API>"
        }

    ## 4: Detail Metadata Payload


    # Metadata Listing
    """
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer,)

    @method_decorator(login_required)
    def get(self, request, format=None):
        resp = OrderedDict()
        errors = []

        for model_cls, url_name_dict in MODEL_VIEW_DICT.iteritems():
            try:
                resp[model_cls._meta.verbose_name] = \
                    _lookup_metadata(url_name_dict, request, model_cls, self)
            except Exception as e:
                # There is a good reason for this broad catch
                # Accumulate and report all errors at once ( re-raising )
                LOGGER.exception(e)
                errors.append(e)

        if errors:  # See, our broad Except up there wasn't so evil after all
            raised_exc = ValidationError(detail=errors)
            raised_exc.message = 'Could not create root / metadata view'
            raise raised_exc

        return Response(resp)


def root_redirect_view(request):
    return redirect('api:root_listing', permanent=True)
