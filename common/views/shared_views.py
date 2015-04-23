import logging
import reversion

from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse as django_reverse
from django.conf import settings
from collections import defaultdict
from django.apps import apps
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin

from facilities.models import (
    FacilityOperationState,
    FacilityStatus,
    Facility,
    Owner,
    OwnerType,
    FacilityUpgrade,
    FacilityType
)

from ..metadata import CustomMetadata

METADATA_CLASS = CustomMetadata()
LOGGER = logging.getLogger(__name__)


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


def _get_metadata_from_detail_url(url_name, obj, request):
    url_path = django_reverse(url_name, kwargs={'pk': obj.pk})
    view = resolve(url_path).func.cls(kwargs={'pk': obj.pk})
    view.initial(request, kwargs={'pk': obj.pk})
    return METADATA_CLASS.determine_metadata(request, view)


def _resolve_detail_metadata(request, url_name, model_cls):
    """I am not proud of this"""
    # This is diabolically evil; I am sorry
    # We need to guarantee that a detail object exists for each detail endpoint
    # The default metadata API will not resolve the actions otherwise
    # If called on a live system, it may cause sequence fields to "skip"
    # There is a plan to do our own metadata implementation; it will be cleaner

    from model_mommy import mommy  # Late import because of embarassment

    if not model_cls.objects.count():  # Do this only if there is no record

        # hack to cater for the validation in transitions

        if model_cls == FacilityOperationState:
            status = mommy.make(FacilityStatus, name='PENDING_OPENING')
            status_2 = mommy.make(FacilityStatus, name='OPERATIONAL')
            facility = mommy.make(Facility, operation_status=status)
            obj = mommy.make(
                FacilityOperationState, facility=facility,
                operation_status=status_2)
            metadata = _get_metadata_from_detail_url(url_name, obj, request)
            FacilityOperationState.objects.filter(
                facility=facility).all().delete()
            facility.delete()
            status.delete()
            status_2.delete()
        elif model_cls == FacilityUpgrade:
            owner_type = mommy.make(OwnerType, name='PRIVATE')
            owner = mommy.make(Owner, owner_type=owner_type)
            facility_type = mommy.make(FacilityType, name='MATERNITY_HOME')
            facility_type_upgrade = mommy.make(
                FacilityType, name='LOWEST_LEVEL_HOSPITAL')
            facility = mommy.make(
                Facility, name='Mbagathi hosi', facility_type=facility_type,
                owner=owner)

            obj = mommy.make(
                FacilityUpgrade, facility_type=facility_type_upgrade,
                facility=facility)
            metadata = _get_metadata_from_detail_url(url_name, obj, request)
            FacilityUpgrade.objects.filter(facility=facility).all().delete()
            facility.delete()
            facility_type.delete()
            facility_type_upgrade.delete()
            owner.delete()
            owner_type.delete()

        else:
            obj = mommy.make(model_cls)
            metadata = _get_metadata_from_detail_url(url_name, obj, request)
            obj.delete()
    else:
        obj = model_cls.objects.all()[:1][0]
        metadata = _get_metadata_from_detail_url(url_name, obj, request)

    return metadata


def _lookup_metadata(url_name_dict, request, model_cls):
    """
    This is what composes the final payload that goes to the client
    """
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
                url_name_dict['detail_url'],
                model_cls
            )
    }


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
        resp = {}
        errors = []

        for model_cls, url_name_dict in MODEL_VIEW_DICT.iteritems():
            try:
                resp[model_cls._meta.verbose_name] = \
                    _lookup_metadata(url_name_dict, request, model_cls)
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
