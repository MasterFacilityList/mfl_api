from django.conf import settings

import django_filters
from .search_utils import ElasticAPI


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
