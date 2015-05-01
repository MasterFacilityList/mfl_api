from rest_framework import filters


class CountyAndNationalUserFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to list facilities in their county
    if they are not a national user.

    This complements the fairly standard ( django.contrib.auth )
    permissions setup.

    It is not intended to be applied to all views ( it should be used
    only on views for resources that are directly linked to counties
    e.g. facilities ).
    """
    def filter_queryset(self, request, queryset, view):
        # The line below reflects the fact that geographic "attachment"
        # will occur at the smallest unit i.e the ward
        if not request.user.is_national and request.user.county \
                and hasattr(queryset.model, 'ward'):
            return queryset.filter(
                ward__constituency__county=request.user.county)

        return queryset
