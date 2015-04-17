from django.core.http import url, patterns

from .views import(
    CommunityHealthUnitListView,
    CommunityHealthUnitDetailView,
    CommunityHealthWorkerListView,
    CommunityHealthWorkerDetailView,
    CommunityHealthWorkerContacttListView,
    CommunityHealthWorkerContactDetailView)


urlpatterns = patterns(
    '',
    url(r'^$', CommunityHealthUnitListView.as_view(),
        name='communit_units_list'),
    url(r'^(?P<pk>[^/]+)',
        CommunityHealthUnitDetailView.as_view,
        name='community_detail_view'),

    url(r'^$', CommunityHealthWorkerListView.as_view(),
        name='communit_units_list'),
    url(r'^(?P<pk>[^/]+)',
        CommunityHealthWorkerDetailView.as_view,
        name=""),

    url(r'^$', CommunityHealthWorkerContacttListView.as_view(),
        name='communit_units_list'),
    url(r'^(?P<pk>[^/]+)',
        CommunityHealthWorkerContactDetailView.as_view(),
        name="")
)
