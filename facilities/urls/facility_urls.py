from django.conf.urls import url, patterns

from .. import views


urlpatterns = patterns(
    '',

    url(r'^material/$',
        views.FacilityExportMaterialListView.as_view(),
        name='material'),

    url(r'^flattened_categories/$',
        views.FlattenedCategories.as_view(),
        name='flattened_categories'),

    url(r'^regulator_sync_update/(?P<pk>[^/]+)/$',
        views.RegulatorSyncUpdateView.as_view(),
        name='regulator_sync_update'),

    url(r'^regulator_sync/(?P<pk>[^/]+)/$',
        views.RegulatorSyncDetailView.as_view(),
        name='regulator_sync_detail'),

    url(r'^regulator_sync/$',
        views.RegulatorSyncListView.as_view(),
        name='regulator_syncs_list'),

    url(r'^option_group_with_options/$',
        views.PostOptionGroupWithOptionsView.as_view(),
        name='post_option_group_with_options'),

    url(r'^option_group_with_options/(?P<pk>[^/]+)/$',
        views.PostOptionGroupWithOptionsView.as_view(),
        name='delete_option_group_with_options'),

    url(r'^level_change_reasons/$',
        views.FacilityLevelChangeReasonListView.as_view(),
        name='facility_level_change_reasons_list'),
    url(r'^level_change_reasons/(?P<pk>[^/]+)/$',
        views.FacilityLevelChangeReasonDetailView.as_view(),
        name='facility_level_change_reason_detail'),

    url(r'^keph/$', views.KephLevelListView.as_view(),
        name='keph_levels_list'),
    url(r'^keph/(?P<pk>[^/]+)/$',
        views.KephLevelDetailView.as_view(),
        name='keph_level_detail'),

    url(r'^officer_facade/$',
        views.CustomFacilityOfficerView.as_view(),
        name='officer_facade_create'),

    url(r'^officer_facade/(?P<facility_id>[^/]+)/$',
        views.CustomFacilityOfficerView.as_view(),
        name='officer_facade_list'),

    url(r'^officer_facade/delete/(?P<pk>[^/]+)/$',
        views.CustomFacilityOfficerView.as_view(),
        name='officer_facade_delete'),

    url(r'^facility_updates/$',
        views.FacilityUpdatesListView.as_view(),
        name='facility_updatess_list'),
    url(r'^facility_updates/(?P<pk>[^/]+)/$',
        views.FacilityUpdatesDetailView.as_view(),
        name='facility_updates_detail'),

    url(r'^facility_unit_regulation/$',
        views.FacilityUnitRegulationListView.as_view(),
        name='facility_unit_regulations_list'),
    url(r'^facility_unit_regulation/(?P<pk>[^/]+)/$',
        views.FacilityUnitRegulationDetailView.as_view(),
        name='facility_unit_regulation_detail'),

    url(r'^regulatory_body_users/$',
        views.RegulatoryBodyUserListView.as_view(),
        name='regulatory_body_users_list'),
    url(r'^regulatory_body_users/(?P<pk>[^/]+)/$',
        views.RegulatoryBodyUserDetailView.as_view(),
        name='regulatory_body_user_detail'),

    url(r'^facility_officers/$', views.FacilityOfficerListView.as_view(),
        name='facility_officers_list'),
    url(r'^facility_officers/(?P<pk>[^/]+)/$',
        views.FacilityOfficerDetailView.as_view(),
        name='facility_officer_detail'),

    url(r'^dashboard/$', views.DashBoard.as_view(), name='dashboard'),

    url(r'^facility_correction_template/(?P<pk>[^/]+)/$',
        views.FacilityCorrectionTemplate.as_view(),
        name='facility_correction_template'),

    url(r'^facility_inspection_report/(?P<pk>[^/]+)/$',
        views.FacilityInspectionReport.as_view(),
        name='facility_inspection_report'),

    url(r'^facility_cover_report/(?P<pk>[^/]+)/$',
        views.FacilityCoverTemplate.as_view(),
        name='facility_cover_report'),

    url(r'^facility_detail_report/(?P<pk>[^/]+)/$',
        views.FacilityDetailTemplate.as_view(),
        name='facility_detail_report'),

    url(r'^regulating_body_contacts/$',
        views.RegulatingBodyContactListView.as_view(),
        name='regulating_body_contacts_list'),
    url(r'^regulating_body_contacts/(?P<pk>[^/]+)/$',
        views.RegulatingBodyContactDetailView.as_view(),
        name='regulating_body_contact_detail'),

    url(r'^facility_upgrade/$',
        views.FacilityUpgradeListView.as_view(),
        name='facility_upgrades_list'),
    url(r'^facility_upgrade/(?P<pk>[^/]+)/$',
        views.FacilityUpgradeDetailView.as_view(),
        name='facility_upgrade_detail'),

    url(r'^facility_operation_state/$',
        views.FacilityOperationStateListView.as_view(),
        name='facility_operation_states_list'),
    url(r'^facility_operation_state/(?P<pk>[^/]+)/$',
        views.FacilityOperationStateDetailView.as_view(),
        name='facility_operation_state_detail'),

    url(r'^facility_approvals/$', views.FacilityApprovalListView.as_view(),
        name='facility_approvals_list'),
    url(r'^facility_approvals/(?P<pk>[^/]+)/$',
        views.FacilityApprovalDetailView.as_view(),
        name='facility_approval_detail'),

    url(r'^facility_service_ratings/$',
        views.FacilityServiceRatingListView.as_view(),
        name='facility_service_ratings_list'),
    url(r'^facility_service_ratings/(?P<pk>[^/]+)/$',
        views.FacilityServiceRatingDetailView.as_view(),
        name='facility_service_rating_detail'),

    url(r'^service_categories/$',
        views.ServiceCategoryListView.as_view(),
        name='service_categories_list'),
    url(r'^service_categories/(?P<pk>[^/]+)/$',
        views.ServiceCategoryDetailView.as_view(),
        name='service_category_detail'),

    url(r'^services/$', views.ServiceListView.as_view(), name='services_list'),
    url(r'^services/(?P<pk>[^/]+)/$', views.ServiceDetailView.as_view(),
        name='service_detail'),

    url(r'^options/$', views.OptionListView.as_view(), name='options_list'),
    url(r'^options/(?P<pk>[^/]+)/$', views.OptionDetailView.as_view(),
        name='option_detail'),

    url(r'^facility_services/$', views.FacilityServiceListView.as_view(),
        name='facility_services_list'),
    url(r'^facility_services/(?P<pk>[^/]+)/$',
        views.FacilityServiceDetailView.as_view(),
        name='facility_service_detail'),

    url(r'^facility_units/$', views.FacilityUnitsListView.as_view(),
        name='facility_units_list'),
    url(r'^facility_units/(?P<pk>[^/]+)/$',
        views.FacilityUnitDetailView.as_view(),
        name='facility_unit_detail'),

    url(r'^regulating_bodies/$', views.RegulatingBodyListView.as_view(),
        name='regulating_bodies_list'),
    url(r'^regulating_bodies/(?P<pk>[^/]+)/$',
        views.RegulatingBodyDetailView.as_view(),
        name='regulating_body_detail'),

    url(r'^facility_types/$', views.FacilityTypeListView.as_view(),
        name='facility_types_list'),
    url(r'^facility_types/(?P<pk>[^/]+)/$',
        views.FacilityTypeDetailView.as_view(),
        name='facility_type_detail'),

    url(r'^facility_status/$', views.FacilityStatusListView.as_view(),
        name='facility_statuses_list'),
    url(r'^facility_status/(?P<pk>[^/]+)/$',
        views.FacilityStatusDetailView.as_view(),
        name='facility_status_detail'),

    url(r'^officer_contacts/$', views.OfficerContactListView.as_view(),
        name='officer_contacts_list'),
    url(r'^officer_contacts/(?P<pk>[^/]+)/$',
        views.OfficerContactDetailView.as_view(),
        name='officer_contact_detail'),

    url(r'^job_titles/$', views.JobTitleListView.as_view(),
        name='job_titles_list'),
    url(r'^job_titles/(?P<pk>[^/]+)/$', views.JobTitleDetailView.as_view(),
        name='job_title_detail'),

    url(r'^facility_regulation_status/$',
        views.FacilityRegulationStatusListView.as_view(),
        name='facility_regulation_statuses_list'),
    url(r'^facility_regulation_status/(?P<pk>[^/]+)/$',
        views.FacilityRegulationStatusDetailView.as_view(),
        name='facility_regulation_status_detail'),

    url(r'^regulation_status/$', views.RegulationStatusListView.as_view(),
        name='regulation_statuses_list'),
    url(r'^regulation_status/(?P<pk>[^/]+)/$',
        views.RegulationStatusDetailView.as_view(),
        name='regulation_status_detail'),

    url(r'^officers/$', views.OfficerListView.as_view(),
        name='officers_in_charge_list'),
    url(r'^officers_incharge/(?P<pk>[^/]+)/$',
        views.OfficerDetailView.as_view(),
        name='officer_detail'),

    url(r'^owner_types/$', views.OwnerTypeListView.as_view(),
        name='owner_types_list'),
    url(r'^owner_types/(?P<pk>[^/]+)/$', views.OwnerTypeDetailView.as_view(),
        name='owner_type_detail'),

    url(r'^owners/$', views.OwnerListView.as_view(), name='owners_list'),
    url(r'^owners/(?P<pk>[^/]+)/$', views.OwnerDetailView.as_view(),
        name='owner_detail'),

    url(r'^contacts/$', views.FacilityContactListView .as_view(),
        name='facility_contacts_list'),
    url(r'^contacts/(?P<pk>[^/]+)/$',
        views.FacilityContactDetailView.as_view(),
        name='facility_contact_detail'),

    url(r'^facilities_list/$', views.FacilityListReadOnlyView.as_view(),
        name='facilities_read_list'),
    url(r'^facilities/$',
        views.FacilityListView.as_view(), name='facilities_list'),
    url(r'^facilities/(?P<pk>[^/]+)/$', views.FacilityDetailView.as_view(),
        name='facility_detail'),

    url(r'^option_groups/$',
        views.OptionGroupListView.as_view(),
        name='option_groups_list'),
    url(r'^option_groups/(?P<pk>[^/]+)/$',
        views.OptionGroupDetailView.as_view(),
        name='option_group_detail'),


    url(r'^facility_depts/$',
        views.FacilityDepartmentListView.as_view(),
        name='facility_depts_list'),
    url(r'^facility_depts/(?P<pk>[^/]+)/$',
        views.FacilityDepartmentDetailView.as_view(),
        name='facility_depts_detail'),
)
