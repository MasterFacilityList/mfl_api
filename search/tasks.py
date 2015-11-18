import pydoc
import logging

from django.core.mail import mail_admins
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from common.models import ErrorQueue
from search.search_utils import index_instance


LOGGER = logging.getLogger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/2')),
    name="try_indexing_failed_records",
    ignore_result=True)
def retry_indexing():
    """
    Indexes the the objects that were not indexed on save
    """

    objects_with_errors = ErrorQueue.objects.filter(
        error_type='SEARCH_INDEXING_ERROR')
    for obj in objects_with_errors:
        obj_path = "{}.models.{}".format(obj.app_label, obj.model_name)
        model = pydoc.locate(obj_path)

        try:
            instance = model.objects.get(id=obj.object_pk)
            result = index_instance(
                instance._meta.app_label,
                instance.__class__.__name__,
                instance.id)
            if result:
                obj.delete()
            else:
                obj.retries = obj.retries + 1
                if obj.retries > 2:
                    mail_admins(
                        subject="Update Search Index Error",
                        message="Indexing failed records is failing."
                        " Please check and ensure elasticsearch is up"
                    )
                obj.save()
        except model.DoesNotExist:
            # The related object is already deleted in the database
            LOGGER.info("The record to be indexed has been deleted")
