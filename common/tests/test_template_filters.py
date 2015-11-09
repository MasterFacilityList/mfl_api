from django.conf import settings
from django.test import TestCase
from django.template import Template, Context


class TestTemplateTags(TestCase):

    def test_true_filter(self):
        template = (
            "{% load mfl_filter %}"
            "{{attribute | mfl_bool_none_date_filter}}"
        )
        context = Context({
            "attribute": True
        })
        tpl = Template(template)
        val = tpl.render(context)
        self.assertEqual(val, "Yes")

    def test_false_filter(self):
        template = (
            "{% load mfl_filter %}"
            "{{attribute | mfl_bool_none_date_filter}}"
        )
        context = Context({
            "attribute": False
        })
        tpl = Template(template)
        val = tpl.render(context)
        self.assertEqual(val, "No")

    def test_none_filter(self):
        template = (
            "{% load mfl_filter %}"
            "{{attribute | mfl_bool_none_date_filter}}"
        )
        context = Context({
            "attribute": None
        })
        tpl = Template(template)
        val = tpl.render(context)
        self.assertEqual(val, "Not Applicable")

    def test_datetime_filter(self):
        template = (
            "{% load mfl_filter %}"
            "{{attribute | mfl_bool_none_date_filter}}"
        )
        context = Context({
            "attribute": "2015-11-09T10:34:47.892271Z"
        })
        tpl = Template(template)
        val = tpl.render(context)
        self.assertEqual(val, "2015 - 11 - 9")

    def test_date_filter(self):
        template = (
            "{% load mfl_filter %}"
            "{{attribute | mfl_bool_none_date_filter}}"
        )
        context = Context({
            "attribute": "2015-11-09"
        })
        tpl = Template(template)
        val = tpl.render(context)
        self.assertEqual(val, "2015 - 11 - 9")

    def test_non_filterable_value(self):
        template = (
            "{% load mfl_filter %}"
            "{{attribute | mfl_bool_none_date_filter}}"
        )
        context = Context({
            "attribute": "afafaf"
        })
        tpl = Template(template)
        val = tpl.render(context)
        self.assertEqual(val, "afafaf")
