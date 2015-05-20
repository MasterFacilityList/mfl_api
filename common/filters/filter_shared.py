import django_filters

from django import forms
from django.utils.encoding import force_str
from django.utils.dateparse import parse_datetime
from django.conf import settings

from rest_framework import ISO_8601

from search.search_utils import ElasticAPI


class IsoDateTimeField(forms.DateTimeField):
    """
    It support 'iso-8601' date format too which is out the scope of
    the ``datetime.strptime`` standard library

    # ISO 8601: ``http://www.w3.org/TR/NOTE-datetime``
    """
    def strptime(self, value, format):
        value = force_str(value)
        if format == ISO_8601:
            parsed = parse_datetime(value)
            if parsed is None:  # Continue with other formats if doesn't match
                raise ValueError
            return parsed
        return super(IsoDateTimeField, self).strptime(value, format)


class IsoDateTimeFilter(django_filters.DateTimeFilter):
    """ Extend ``DateTimeFilter`` to filter by ISO 8601 formated dates too"""
    field_class = IsoDateTimeField


class SearchFilter(django_filters.filters.Filter):
    """
    Given a query searches elastic search index and returns a queryset of hits.
    """

    def filter(self, qs, value):
        super(SearchFilter, self).filter(qs, value)
        api = ElasticAPI()

        document_type = qs.model.__name__.lower()
        index_name = settings.SEARCH.get('INDEX_NAME')
        result = api.search_document(index_name, document_type, value)

        hits = []
        try:
            hits = result.json().get('hits').get('hits') if result.json() \
                else hits
        except AttributeError:
            hits = hits
        hits_ids_list = []

        for hit in hits:
            obj_id = hit.get('_id')
            hits_ids_list.append(obj_id)

        hits_qs = qs.model.objects.filter(id__in=hits_ids_list)

        # the filter function expects a queryset and not a list
        # hence the need to convert the list back to queryset
        combined_results = list(set(hits_qs).intersection(qs))
        combined_results_ids = [obj.id for obj in combined_results]
        final_queryset = qs.model.objects.filter(id__in=combined_results_ids)

        return final_queryset


class ListFilterMixin(object):
    """
    Enable filtering by comma separated values.

    eg ?number=1,2,3&name=a,b

    Apply this mixin to a type of django_filters.Filter that
    filters character strings. To filter a different type,
    override the customize method in the filter that this
    mixin is mixed into.

    For an example, look at ListCharFilter, ListIntegerFilter below.
    """

    def sanitize(self, value_list):
        """
        remove empty items
        """
        return [v for v in value_list if v != u'']

    def customize(self, value):
        return value

    def filter(self, qs, value):
        multiple_vals = value.split(u",")
        multiple_vals = self.sanitize(multiple_vals)
        multiple_vals = map(self.customize, multiple_vals)
        actual_filter = django_filters.fields.Lookup(multiple_vals, 'in')
        return super(ListFilterMixin, self).filter(qs, actual_filter)


class ListCharFilter(ListFilterMixin, django_filters.CharFilter):
    """
    Enable filtering of comma separated strings.
    """
    pass


class ListIntegerFilter(ListCharFilter):
    """
    Enable filtering of comma separated integers.
    """

    def customize(self, value):
        return int(value)


class CommonFieldsFilterset(django_filters.FilterSet):
    """Every model that descends from AbstractBase should have this

    The usage pattern for this is presently simplistic; mix it in, then add to
    the `fields` in the filter's `Meta` `'updated', 'created',
    updated_before', 'created_before', 'updated_after', 'created_after'' and
    any other applicable / extra fields.

    When you inherit this, DO NOT add a `fields` declaration. Let the implicit
    filter fields ( every model field gets one ) stay in place.
    """
    updated_before = IsoDateTimeFilter(
        name='updated', lookup_type='lte',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))
    created_before = IsoDateTimeFilter(
        name='created', lookup_type='lte',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))

    updated_after = IsoDateTimeFilter(
        name='updated', lookup_type='gte',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))
    created_after = IsoDateTimeFilter(
        name='created', lookup_type='gte',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))

    updated_on = IsoDateTimeFilter(
        name='updated', lookup_type='exact',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))
    created_on = IsoDateTimeFilter(
        name='created', lookup_type='exact',
        input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))

    is_deleted = django_filters.BooleanFilter(
        name='deleted', lookup_type='exact')
    is_active = django_filters.BooleanFilter(
        name='active', lookup_type='exact')
    search = SearchFilter(name='search')
