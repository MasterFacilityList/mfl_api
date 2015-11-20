import pydoc
import logging

from django.core.mail import mail_admins

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from common.models import ErrorQueue
from users.models import send_email_on_signup, MflUser


LOGGER = logging.getLogger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="try_sending_failed_emails",
    ignore_result=True)
def resend_user_signup_emails():
    """
    Resends emails that failed to be sent during user registration
    """

    objects_with_errors = ErrorQueue.objects.filter(
        error_type='SEND_EMAIL_ERROR')
    for obj in objects_with_errors:
        obj_path = "{0}.models.{1}".format(obj.app_label, obj.model_name)
        model = pydoc.locate(obj_path)
        try:
            instance = model.objects.get(id=obj.object_pk)
            user_id = instance.id
            email = instance.email
            first_name = instance.first_name
            employee_number = instance.employee_number
            mail_sent = send_email_on_signup(
                user_id, email, first_name, employee_number)
            if mail_sent:
                obj.delete()
            else:
                obj.retries = obj.retries + 1
                obj.save()
                mail_admins(
                    subject="Send User Email Error",
                    message="Sending emails to users on registration is "
                    "failing. Check the email settings in the environment"
                ) if obj.retries > 2 else None
        except MflUser.DoesNotExist:
            LOGGER.info("The user has been deleted")
