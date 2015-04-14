import django_filters

from .models import Contact, Constituency, Ward, UserCounties


class ContactFilter(django_filters.FilterSet):
    class Meta:
        model = Contact


class ConstituencyFilter(django_filters.FilterSet):
    class Meta:
        model = Constituency


class WardFilter(django_filters.FilterSet):
    class Meta:
        model = Ward


class UserCountiesFilter(django_filters.FilterSet):
    class Meta:
        model = UserCounties
