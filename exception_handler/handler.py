from django.core.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status

import logging

LOGGER = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Django Restframework fails silently to the errors it doesn't handle.
    This handler will bubble up errors that are not handled by DRF.
    Users of this handler will have to catch the error themselves..
    ..NOTE : ValidationErrors esp django model errors are context specific
    hence handling them here will provide a generic message that won't
    be helpful for that context..therefore they are better handled by the
    users themselves.
    """

    response = exception_handler(exc, context)
    if response:
        return response

    if isinstance(exc, ValidationError):
        LOGGER.error(exc)
        return Response(exc, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {'detail': ['Server Error: {}'.format(exc.__class__.__name__)]}

        # Keep this or you'll pull your hair out when **** hits the fan
        import traceback
        traceback.print_exc()
        LOGGER.error(exc)
        return Response(data, status=500)
