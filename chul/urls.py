from django.conf.urls import url, patterns

from .views import(
    CommunityHealthUnitListView,
    CommunityHealthUnitDetailView,
    CommunityHealthWorkerListView,
    CommunityHealthWorkerDetailView,
    CommunityHealthWorkerContactListView,
    CommunityHealthWorkerContactDetailView,
    StatusListView,
    StatusDetailView,
    CommunityListView,
    CommunityDetailView,
    CommunityHealthUnitContactListView,
    CommunityHealthUnitContactDetailView,
    ApproverListView,
    ApproverDetailView,
    CommunityHealthUnitApprovalListView,
    CommunityHealthUnitApprovalDetailView,
    CommunityHealthWorkerApprovalListView,
    CommunityHealthWorkerApprovalDetailView,
    ApprovalStatusListView,
    ApprovalStatusDetailView
)


urlpatterns = patterns(
    '',
    url(r'^statuses_list/$', StatusListView.as_view(),
        name='statuses_list'),
    url(r'^statuses/(?P<pk>[^/]+)/$',
        StatusDetailView.as_view(),
        name="status_detail"),

    url(r'^communities/$', CommunityListView.as_view(),
        name='communities_list'),
    url(r'^communities/(?P<pk>[^/]+)/$',
        CommunityDetailView.as_view(),
        name="community_detail"),

    url(r'^unit_contacts/$', CommunityHealthUnitContactListView.as_view(),
        name='community_health_unit_contacts_list'),
    url(r'^unit_contacts/(?P<pk>[^/]+)/$',
        CommunityHealthUnitContactDetailView.as_view(),
        name="community_health_unit_contact_detail"),

    url(r'^approvers/$', ApproverListView.as_view(),
        name='approvers_list'),
    url(r'^approvers/(?P<pk>[^/]+)/$',
        ApproverDetailView.as_view(),
        name="approver_detail"),

    url(r'^unit_approvals/$', CommunityHealthUnitApprovalListView.as_view(),
        name='community_health_unit_approvals_list'),
    url(r'^unit_approvals/(?P<pk>[^/]+)/$',
        CommunityHealthUnitApprovalDetailView.as_view(),
        name="community_health_unit_approval_detail"),

    url(r'^worker_approvals/$',
        CommunityHealthWorkerApprovalListView.as_view(),
        name='community_health_worker_approvals_list'),
    url(r'^worker_approvals/(?P<pk>[^/]+)/$',
        CommunityHealthWorkerApprovalDetailView.as_view(),
        name="community_health_worker_approval_detail"),

    url(r'^approval_statuses/$', ApprovalStatusListView.as_view(),
        name='approval_statuses_list'),
    url(r'^approval_statuses/(?P<pk>[^/]+)/$',
        ApprovalStatusDetailView.as_view(),
        name="approval_status_detail"),

    url(r'^workers/$', CommunityHealthWorkerListView.as_view(),
        name='community_health_workers_list'),
    url(r'^workers/(?P<pk>[^/]+)/$',
        CommunityHealthWorkerDetailView.as_view(),
        name="community_health_worker_detail"),


    url(r'^workers_contacts/$', CommunityHealthWorkerContactListView.as_view(),
        name='community_health_worker_contacts_list'),
    url(r'^workers_contacts/(?P<pk>[^/]+)/$',
        CommunityHealthWorkerContactDetailView.as_view(),
        name="community_health_worker_contact_detail"),


    url(r'^units/$', CommunityHealthUnitListView.as_view(),
        name='community_health_units_list'),
    url(r'^units/(?P<pk>[^/]+)/$',
        CommunityHealthUnitDetailView.as_view(),
        name='community_health_unit_detail'),
)
