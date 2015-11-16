from mock import patch
from socket import gaierror

from django.core.management import call_command

from common.tests.test_models import BaseTestCase
from common.models import ErrorQueue
from ..models import MflUser


class TestMflUserModel(BaseTestCase):

    def test_send_email_failure(self):
        with patch('django.core.mail.EmailMultiAlternatives.send') as socket_mock:  # noqa
            socket_mock.side_effect = gaierror
            MflUser.objects.create_user(
                email='mimi@wewe.com',
                first_name='wao',
                last_name='yule',
                employee_number='sdfsd44',
                password='yule454858345')
            # Network is unreachable hence email not sent
            self.assertEquals(1, ErrorQueue.objects.count())

    def test_send_email_success(self):
        MflUser.objects.create_user(
            email='mimi@wewe.com',
            first_name='wao',
            last_name='yule',
            employee_number='sdfsd44',
            password='yule454858345')
        self.assertEquals(0, ErrorQueue.objects.count())

    def test_retry_sending_failed_emails_failure(self):
        with patch('django.core.mail.EmailMultiAlternatives.send') as socket_mock:   # noqa
            socket_mock.side_effect = gaierror
            MflUser.objects.create_user(
                email='mimi@wewe.com',
                first_name='wao',
                last_name='yule',
                employee_number='sdfsd44',
                password='yule454858345')
            # Network is unreachable hence email not sent
            self.assertEquals(1, ErrorQueue.objects.count())
            call_command("resend_user_emails")

            # the network is still unreachable hence not email sent
            self.assertEquals(1, ErrorQueue.objects.count())

    def test_retry_sending_failed_emails_success(self):
        with patch('django.core.mail.EmailMultiAlternatives.send') as socket_mock:   # noqa
            socket_mock.side_effect = gaierror
            MflUser.objects.create_user(
                email='mimi@wewe.com',
                first_name='wao',
                last_name='yule',
                employee_number='sdfsd44',
                password='yule454858345')
            # Network is unreachable hence email not sent
            self.assertEquals(1, ErrorQueue.objects.count())
        call_command("resend_user_emails")
        # the network is now reachable hence email sent
        self.assertEquals(0, ErrorQueue.objects.count())

    def test_retry_sending_email_related_object_deleted(self):
        with patch('django.core.mail.EmailMultiAlternatives.send') as socket_mock:   # noqa
            socket_mock.side_effect = gaierror
            user = MflUser.objects.create_user(
                email='mimi@wewe.com',
                first_name='wao',
                last_name='yule',
                employee_number='sdfsd44',
                password='yule454858345')
            # Network is unreachable hence email not sent
            self.assertEquals(1, ErrorQueue.objects.count())
            user.delete()
            call_command("resend_user_emails")

            # the network is still unreachable hence not email sent
            self.assertEquals(1, ErrorQueue.objects.count())
