from django.test import TestCase
from django.template import Template, Context


class TestTemplateTags(TestCase):
    """
    Test the custom filters class
    """

    def test_true_filter(self):
        """
        Test True is converted to Yes
        """
        template = (
            "{% load mfl_none_filter %}"
            "{{attribute | mfl_bool_none_date_filter}}"
        )
        context = Context({
            "attribute": True
        })
        tpl = Template(template)
        val = tpl.render(context)
        self.assertEqual(val, "Yes")

    def test_false_filter(self):
        """
        Test False is converted to No
        """
        template = (
            "{% load mfl_none_filter %}"
            "{{attribute | mfl_bool_none_date_filter}}"
        )
        context = Context({
            "attribute": False
        })
        tpl = Template(template)
        val = tpl.render(context)
        self.assertEqual(val, "No")

    def test_none_filter(self):
        """
        Test None is converted to Not Applicable
        """
        template = (
            "{% load mfl_none_filter %}"
            "{{attribute | mfl_bool_none_date_filter}}"
        )
        context = Context({
            "attribute": None
        })
        tpl = Template(template)
        val = tpl.render(context)
        self.assertEqual(val, "Not Applicable")

    def test_datetime_filter(self):
        """
        Test Datetime is converted to date only
        """
        template = (
            "{% load mfl_none_filter %}"
            "{{attribute | mfl_bool_none_date_filter}}"
        )
        context = Context({
            "attribute": "2015-11-09T10:34:47.892271Z"
        })
        tpl = Template(template)
        val = tpl.render(context)
        self.assertEqual(val, "2015 - 11 - 9")

    def test_date_filter(self):
        """
        Test date is converted to a good human format
        """
        template = (
            "{% load mfl_none_filter %}"
            "{{attribute | mfl_bool_none_date_filter}}"
        )
        context = Context({
            "attribute": "2015-11-09"
        })
        tpl = Template(template)
        val = tpl.render(context)
        self.assertEqual(val, "2015 - 11 - 9")

    def test_non_filterable_value(self):
        """
        Test anything that is not handled by the filter is retained
        """
        template = (
            "{% load mfl_none_filter %}"
            "{{attribute | mfl_bool_none_date_filter}}"
        )
        context = Context({
            "attribute": "afafaf"
        })
        tpl = Template(template)
        val = tpl.render(context)
        self.assertEqual(val, "afafaf")
