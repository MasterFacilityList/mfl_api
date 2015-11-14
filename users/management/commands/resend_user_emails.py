import pydoc

from django.core.management import BaseCommand
from common.models import ErrorQueue
from users.models import send_email_on_signup


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
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
                send_email_on_signup(
                    user_id, email, first_name, employee_number)
                obj.delete()
            except:
                pass
