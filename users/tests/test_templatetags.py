from django.conf import settings
from django.test import TestCase
from django.template import Template, Context


class TestTemplateTags(TestCase):

    def test_reset_link(self):
        template_file = (
            "{% load dj_settings %}"
            "{% reset_link uid=uid token=token %}"
        )
        context = {
            "uid": "yyyy",
            "token": "1234567"
        }
        tpl = Template(template_file)
        val = tpl.render(Context(context))
        self.assertEqual(
            val,
            "{}/#/reset_pwd_confirm/yyyy/1234567".format(settings.FRONTEND_URL)
        )

    def test_subject_header(self):
        template = (
            "{% load dj_settings %}"
            "{% email_subject %} End"
        )
        tpl = Template(template)
        val = tpl.render(Context())
        self.assertEqual(val, "{} End".format(settings.EMAIL_SUBJECT_PREFIX))
