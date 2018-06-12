"""
Custom search filters.

Add a custom django_filters field that interacts with Elasticsearch
"""

from django.conf import settings
from django.db.models import Q  # NOQA

import django_filters

from search.search_utils import ElasticAPI


FIELD_TYPES = [
    'SequenceField', 'CharField', 'TextField'
]


class SearchFilter(django_filters.filters.Filter):
    """
    Given a query searches elastic search index.

    Returns a django queryset of the model searched.
    """

    api = ElasticAPI()
    search_type = 'full_text'

    def filter(self, qs, value):
        """Override this method in order to search in Elasticsearch index."""
        super(SearchFilter, self).filter(qs, value)
        api = ElasticAPI()
        if api._is_on:

            document_type = qs.model
            index_name = settings.SEARCH.get('INDEX_NAME')
            if self.search_type == 'full_text':
                result = api.search_document(index_name, document_type, value)
            else:
                result = api.search_auto_complete_document(
                    index_name, document_type, value)

            hits = []
            try:
                hits = result.json().get('hits').get('hits') if result.json() \
                    else hits
            except AttributeError:
                hits = hits

            hits_ids_list = [str(hit.get('_id')) for hit in hits]

            pk_list = hits_ids_list

            if qs.model._meta.managed:
                table_name = "{0}_{1}.id".format(
                    qs.model._meta.app_label, qs.model.__name__.lower())
            else:
                table_name = "{}.id".format(qs.model._meta.db_table)

            clauses = ' '.join(
                [
                    "WHEN %s='%s' THEN '%s'" % (
                        table_name, pk, i) for i, pk in enumerate(pk_list)
                ]
            )

            ordering = 'CASE %s END' % clauses
            queryset = qs.filter(pk__in=pk_list).extra(
                select={'ordering': ordering}, order_by=('ordering',))

            return queryset
        else:

            model = qs.model

            fields = [
                field.name for field in model._meta.get_fields()
                if field.concrete and field.get_internal_type() in FIELD_TYPES
            ]

            filter_params = {}

            for field in fields:
                field_type = model._meta.get_field(field).get_internal_type()
                if field_type == 'SequenceField' and value.isdigit():
                    filter_params[field + '__exact'] = value
                    break
                else:
                    filter_params[field + '__icontains'] = value

            q_filter = ""
            for key, value in filter_params.items():
                q_filter += "Q({0}='{1}') | ".format(key, value)

            # remove the pipe character at the end of the string
            q_filter_reverse = q_filter[::-1]
            q_filter = q_filter_reverse[3:len(q_filter_reverse) + 1]
            q_filter = q_filter[::-1]
            return qs.filter(eval(q_filter))


class AutoCompleteSearchFilter(SearchFilter):
    """Autocomplete search filter."""

    search_type = "auto_complete"
