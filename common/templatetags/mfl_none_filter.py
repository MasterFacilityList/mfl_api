from django import template
from django.utils import dateparse


register = template.Library()


@register.filter
def mfl_bool_none_date_filter(value):
    """
    Coverts None to Not Applicable
    """
    if value is True:
        return "Yes"
    elif value is False:
        return "No"
    elif value is None:
        return "Not Applicable"
    elif dateparse.parse_datetime(str(value)):
        obj = dateparse.parse_datetime(str(value))
        return "{0} - {1} - {2}".format(obj.year, obj.month, obj.day)
    elif dateparse.parse_date(str(value)):
        obj = dateparse.parse_date(str(value))
        return "{0} - {1} - {2}".format(obj.year, obj.month, obj.day)
    else:
        return value
