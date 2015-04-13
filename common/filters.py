import django_filters

from .models import Contact, Constituency, SubCounty


class ContactFilter(django_filters.FilterSet):
    class Meta:
        model = Contact


class ConstituencyFilter(django_filters.FilterSet):
    class Meta:
        model = Constituency


class SubCountyFilter(django_filters.FilterSet):
    class Meta:
        model = SubCounty
