import re
from django.conf import settings

import django_filters
from search.search_utils import ElasticAPI
from facilities.models import Facility


class SearchFilter(django_filters.filters.Filter):
    """
    Given a query searches elastic search index and returns a queryset of hits.
    """
    api = ElasticAPI()
    search_type = 'full_text'

    def filter(self, qs, value):
        super(SearchFilter, self).filter(qs, value)
        api = ElasticAPI()

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
        hits_ids_list = []
        hits_and_scores = []

        for hit in hits:
            obj_id = hit.get('_id')
            instance = qs.model.objects.get(id=obj_id)
            score = hit.get('_score')
            instance.search = score
            hits_ids_list.append(str(obj_id))
            hits_and_scores.append({'id': obj_id, 'score': score})

        pk_list = hits_ids_list
        table_name = "{}_{}.id".format(
            qs.model._meta.app_label, qs.model.__name__.lower())
        clauses = ' '.join(
            [
                "WHEN %s='%s' THEN '%s'" % (
                    table_name, pk, i) for i, pk in enumerate(pk_list)
            ]
        )

        ordering = 'CASE %s END' % clauses
        queryset = qs.model.objects.filter(pk__in=pk_list).extra(
            select={'ordering': ordering}, order_by=('ordering',))
        m = re.search('\d+', str(value))
        if m:
            facility = Facility.objects.filter(code=value)
            return facility if facility.count() == 1 else queryset
        else:
            return queryset


class AutoCompleteSearchFilter(SearchFilter):
    search_type = "auto_complete"
