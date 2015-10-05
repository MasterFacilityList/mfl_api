import logging
import reversion

from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.files import FileField, FieldFile
from django.http import HttpResponse
from weasyprint import HTML
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin

from facilities.filters import facility_filters


LOGGER = logging.getLogger(__name__)


class AuditableDetailViewMixin(RetrieveModelMixin):

    def _resolve_field(self, field, version):
        model_class = version.object.__class__
        fallback = version.field_dict.get(field, None)
        try:
            model_field = model_class._meta.get_field(field)
        except FieldDoesNotExist:
            # since `model_class` represents the current representation of the
            # model, what will happen if field is deleted from model ??
            return fallback

        follows = version.revision.version_set.exclude(pk=version.pk)

        if model_field.is_relation:
            followed_model_class = model_field.related_model
            for f in follows:
                if (f.content_type.model_class() == followed_model_class and
                        f.field_dict['id'] == fallback):
                    # What happens to M2M fields?
                    return f.object_repr

        if isinstance(model_field, (FileField, FieldFile, )):
            return version.field_dict[field].name

        return fallback

    def _compare_objs(self, fields, old, new):
        output = []

        for fld in fields:
            old_val = old.field_dict.get(fld, '')
            new_val = new.field_dict.get(fld, '')

            if old_val != new_val:
                output.append({
                    "name": fld,
                    "old": self._resolve_field(fld, old),
                    "new": self._resolve_field(fld, new)
                })

        return output

    def generate_diffs(self, instance, exclude=[]):
        versions = reversion.get_for_object(instance)
        fieldnames = [
            f.name for f in instance._meta.fields
            if f.name not in exclude
        ]
        ans = []
        for i in range(1, len(versions), 1):
            new = versions[i-1]
            old = versions[i]
            diff = self._compare_objs(fieldnames, old, new)
            if diff:
                ans.append({
                    "updates": diff,
                    "updated_by": new.revision.user.get_full_name,
                    "updated_on": new.revision.date_created
                })

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
                instance, exclude=['deleted', 'search'],
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


class DownloadPDFMixin(object):

    def download_file(self, html, file_name):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(
            file_name
        )
        HTML(string=html).write_pdf(response)
        return response
