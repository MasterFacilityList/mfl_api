import logging
import reversion

from collections import OrderedDict
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin

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
    This view serves as the entry point to the entire API.

    It also hosts all the metadata.
    """
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
