DROP MATERIALIZED VIEW IF EXISTS facilities_excel_export;

CREATE MATERIALIZED VIEW facilities_excel_export AS
SELECT facilities_facility.id as id, facilities_facility.search as search,
facilities_facility.name as name, facilities_facility.code as code,
facilities_facility.registration_number, facilities_facility.number_of_beds as beds,
facilities_facility.number_of_cots as cots, common_ward.name as ward_name,
common_ward.id as ward,facilities_facility.approved,facilities_facility.created,
facilities_facility.open_whole_day, facilities_facility.open_public_holidays,
facilities_facility.open_weekends, facilities_facility.open_late_night,
facilities_facility.closed, facilities_facility.is_published,
common_county.name as county_name, common_county.id as county,
common_constituency.name as constituency_name,common_constituency.id as constituency,
common_subcounty.name as sub_county_name,common_subcounty.id as sub_county,
facilities_facilitytype.name as facility_type_name, facilities_facilitytype.id as facility_type,
facilities_kephlevel.name as keph_level_name,facilities_kephlevel.id as keph_level,
facilities_owner.name as owner_name,facilities_owner.id as owner,
facilities_ownertype.name as owner_type_name,facilities_ownertype.id as owner_type,
facilities_regulatingbody.name as regulatory_body_name,facilities_regulatingbody.id as regulatory_body,
facilities_facilitystatus.name as operation_status_name, facilities_facilitystatus.id as operation_status,
facilities_facilitystatus.is_public_visible as is_public_visible,
array(select distinct service_id from facilities_facilityservice where facilities_facilityservice.facility_id=facilities_facility.id) as services,
array(select distinct category_id from facilities_facilityservice inner join facilities_service on facilities_service.id=facilities_facilityservice.service_id where facilities_facilityservice.facility_id=facilities_facility.id) as categories

FROM facilities_facility
LEFT JOIN facilities_kephlevel ON facilities_kephlevel.id = facilities_facility.keph_level_id
LEFT JOIN facilities_owner ON facilities_owner.id = facilities_facility.owner_id
LEFT JOIN facilities_ownertype ON facilities_owner.owner_type_id = facilities_ownertype.id
LEFT JOIN facilities_facilitytype ON facilities_facilitytype.id = facilities_facility.facility_type_id
LEFT JOIN facilities_regulatingbody ON facilities_regulatingbody.id = facilities_facility.regulatory_body_id
LEFT JOIN facilities_facilitystatus ON facilities_facilitystatus.id = facilities_facility.operation_status_id
LEFT JOIN common_ward ON  common_ward.id = facilities_facility.ward_id
LEFT JOIN common_constituency ON  common_constituency.id = common_ward.constituency_id
LEFT JOIN common_subcounty ON  common_subcounty.id = common_ward.sub_county_id
LEFT JOIN common_county ON  common_county.id = common_constituency.county_id;

DROP TRIGGER IF EXISTS refresh_mat_view ON facilities_facility;
create or replace function refresh_mat_view()
returns trigger language plpgsql
as $$
begin
    refresh materialized view facilities_excel_export;
    return null;
end $$;


create trigger refresh_mat_view
after insert or update or delete or truncate
on facilities_facility for each statement
execute procedure refresh_mat_view();
