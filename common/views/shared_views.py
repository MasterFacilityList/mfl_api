import logging
import reversion
import reversion.helpers

from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin

from facilities.filters import facility_filters


LOGGER = logging.getLogger(__name__)


class AuditableDetailViewMixin(RetrieveModelMixin):

    def _compare_objs(self, fields, old, new, include=[]):
        output = []
        for fld in fields:
            comp = reversion.helpers.generate_diffs(old, new, fld, None)
            if len(comp) == 1 and comp[0][0] == 0:
                continue

            obj = {
                i: new.field_dict.get(i, '') for i in include
            }
            obj[fld] = new.field_dict.get(fld, '')
            output.append(obj)

        return output

    def generate_diffs(self, instance, data, exclude=[], include=[]):
        versions = reversion.get_for_object(instance)
        fieldnames = [
            f.name for f in instance._meta.fields
            if f.name not in exclude
        ]
        ans = []
        for i in range(1, len(versions), 1):
            old = versions[i-1]
            new = versions[i]
            diff = self._compare_objs(fieldnames, old, new, include=include)
            if diff:
                ans.append(diff)

        return ans

    def retrieve(self, request, *args, **kwargs):
        """
        A small extension of the default `RetrieveModelMixin` that adds audit.

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
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        audit_requested = (
            str(request.query_params.get('include_audit', None)).lower() in
            facility_filters.TRUTH_NESS
        )
        if audit_requested:
            data["revisions"] = self.generate_diffs(
                instance, data,
                exclude=['deleted', 'search'],
                include=['updated', 'updated_by']
            )

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
