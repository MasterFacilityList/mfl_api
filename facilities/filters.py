import django_filters

from .models import Owner, Service, Facility, FacilityGPS, JobTitle


from common.filters.filter_shared import CommonFieldsFilterset


class JobTitleFilter(CommonFieldsFilterset):
    class Meta:
        model = JobTitle


class OwnerFilter(CommonFieldsFilterset):
    class Meta:
        model = Owner


class ServiceFilter(CommonFieldsFilterset):
    class Meta:
        model = Service


class FacilityGPSFilter(CommonFieldsFilterset):
    class Meta:
        model = FacilityGPS


class FacilityFilter(CommonFieldsFilterset):
    beds = django_filters.NumberFilter(name='number_of_beds')
    cots = django_filters.NumberFilter(name='number_of_cots')
    open_whole_day = django_filters.BooleanFilter(name='open_whole_day')
    open_whole_week = django_filters.BooleanFilter(name='open_whole_week')
    is_classified = django_filters.BooleanFilter(name='is_classified')
    is_published = django_filters.BooleanFilter(name='is_published')

    class Meta:
        model = Facility
