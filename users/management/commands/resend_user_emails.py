from django.core.management import BaseCommand
from ...tasks import resend_user_signup_emails


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        resend_user_signup_emails()
