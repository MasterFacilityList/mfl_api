from mock import patch
from socket import gaierror
from smtplib import SMTPAuthenticationError

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

    def test_send_email_wrong_email_creds_in_settings(self):
        with patch('django.core.mail.EmailMultiAlternatives.send') as socket_mock:  # noqa
            socket_mock.side_effect = SMTPAuthenticationError(
                500, 'authentication failed'
            )
            MflUser.objects.create_user(
                email='mimi@wewe.com',
                first_name='wao',
                last_name='yule',
                employee_number='sdfsd44',
                password='yule454858345')
            # the event is pushed to the error queue due to error
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
            # the object pk does not exist
            ErrorQueue.objects.create(
                object_pk='100000',
                app_label='users',
                model_name='MflUser',
                error_type='SEND_EMAIL_ERROR',
                except_message='Error sending user email')
            # Network is unreachable hence email not sent
            self.assertEquals(1, ErrorQueue.objects.count())
            call_command("resend_user_emails")

            # the user does not exist hence the error record was left as is
            self.assertEquals(1, ErrorQueue.objects.count())

    def test_sending_emails_to_admins(self):
        """
        This is for test coverage purpose only

        Tests that emails are sent to users if the number of retries
        is greater than one
        """

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
            self.assertEquals(1, ErrorQueue.objects.count())
            error_queue_object = ErrorQueue.objects.all()[0]
            self.assertEquals(1, error_queue_object.retries)

            call_command("resend_user_emails")
            self.assertEquals(1, ErrorQueue.objects.count())
            error_queue_object = ErrorQueue.objects.all()[0]
            self.assertEquals(2, error_queue_object.retries)
            error_queue_object.retries = 3
            error_queue_object.save

        call_command("resend_user_emails")
