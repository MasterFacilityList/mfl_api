SELECT COUNT(*) AS zote, COUNT(DISTINCT(common_facilitymapping.mfl_code)) AS zile_unique FROM common_facilitymapping;

DELETE FROM common_facilitymapping WHERE id >= 23542;

SELECT COUNT(*) FROM facilities_facility;

SELECT f.code AS mfl_code,
  f.name AS facility_name,
  ft.name AS facility_type,
  fk.name AS keph_level,
  fo.name AS facility_owner,
  frb.name AS regulatory_body,
  fot.name AS facility_owner_type
FROM facilities_facility AS f
LEFT JOIN facilities_facilitytype AS ft ON f.facility_type_id = ft.id
LEFT JOIN facilities_kephlevel AS fk ON f.keph_level_id = fk.id
LEFT JOIN facilities_owner AS fo ON f.owner_id = fo.id
LEFT JOIN facilities_regulatingbody AS frb ON f.regulatory_body_id = frb.id
LEFT JOIN facilities_ownertype AS fot ON fo.owner_type_id = fot.id
WHERE f.code IS NOT NULL
  AND ft.name IS NOT NULL
  AND fk.name IS NOT NULL
  AND fo.name IS NOT NULL
  AND frb.name IS NOT NULL
  AND fot.name IS NOT NULL;

SELECT f.code AS mfl_code,
  ft.name AS facility_type,
  cogm_ft.dhis_id As facility_type_dhis_id,
  cogm_ft.dhis_name As facility_type_dhis_name,
  fk.name AS keph_level,
  cogm_fk.dhis_id As keph_level_dhis_id,
  cogm_fk.dhis_name As keph_level_dhis_name,
  fo.name AS facility_owner,
  cogm_fo.dhis_id As facility_owner_dhis_id,
  cogm_fo.dhis_name As facility_owner_dhis_name,
  frb.name AS regulatory_body,
  cogm_frb.dhis_id As regulatory_body_dhis_id,
  cogm_frb.dhis_name As regulatory_body_dhis_name,
  fot.name AS facility_owner_type,
  cogm_fot.dhis_id As facility_owner_type_dhis_id,
  cogm_fot.dhis_name As facility_owner_type_dhis_name
FROM facilities_facility AS f
LEFT JOIN facilities_facilitytype AS ft ON f.facility_type_id = ft.id
LEFT JOIN common_orgunitgroupsmapping AS cogm_ft ON cogm_ft.mfl_name = ft.name
LEFT JOIN facilities_kephlevel AS fk ON f.keph_level_id = fk.id
LEFT JOIN common_orgunitgroupsmapping AS cogm_fk ON cogm_fk.mfl_name = 'KEPH ' || fk.name
LEFT JOIN facilities_owner AS fo ON f.owner_id = fo.id
LEFT JOIN common_orgunitgroupsmapping AS cogm_fo ON cogm_fo.mfl_name = fo.name
LEFT JOIN facilities_regulatingbody AS frb ON f.regulatory_body_id = frb.id
LEFT JOIN common_orgunitgroupsmapping AS cogm_frb ON cogm_frb.mfl_name = frb.name
LEFT JOIN facilities_ownertype AS fot ON fo.owner_type_id = fot.id
LEFT JOIN common_orgunitgroupsmapping AS cogm_fot ON cogm_fot.mfl_name = fot.name
WHERE cogm_ft.dhis_id IS NOT NULL
AND cogm_fk.dhis_id IS NOT NULL
AND cogm_fo.dhis_id IS NOT NULL
AND cogm_frb.dhis_id IS NOT NULL
AND cogm_fot.dhis_id IS NOT NULL
ORDER BY f.code ASC;

SELECT f.code AS mfl_code,
  ft.name AS facility_type,
  cogm.dhis_id As facility_type_dhis_id,
  cogm.dhis_name As facility_type_dhis_name,
  fk.name AS keph_level,
  cogm.dhis_id As keph_level_dhis_id,
  cogm.dhis_name As keph_level_dhis_name,
  fo.name AS facility_owner,
  cogm.dhis_id As facility_owner_dhis_id,
  cogm.dhis_name As facility_owner_dhis_name,
  frb.name AS regulatory_body,
  cogm.dhis_id As regulatory_body_dhis_id,
  cogm.dhis_name As regulatory_body_dhis_name,
  fot.name AS facility_owner_type,
  cogm.dhis_id As facility_owner_type_dhis_id,
  cogm.dhis_name As facility_owner_type_dhis_name
FROM facilities_facility AS f
LEFT JOIN facilities_facilitytype AS ft ON f.facility_type_id = ft.id
LEFT JOIN common_orgunitgroupsmapping AS cogm ON cogm.mfl_name = ft.name
LEFT JOIN facilities_kephlevel AS fk ON f.keph_level_id = fk.id
LEFT JOIN facilities_owner AS fo ON f.owner_id = fo.id
LEFT JOIN facilities_regulatingbody AS frb ON f.regulatory_body_id = frb.id
LEFT JOIN facilities_ownertype AS fot ON fo.owner_type_id = fot.id
WHERE f.code IS NOT NULL
  AND ft.name IS NOT NULL
  AND fk.name IS NOT NULL
  AND fo.name IS NOT NULL
  AND frb.name IS NOT NULL
  AND fot.name IS NOT NULL
  AND cogm.dhis_id IS NOT NULL;

SELECT dhis_name, dhis_id FROM common_orgunitgroupsmapping WHERE common_orgunitgroupsmapping.mfl_name = 'Level 2';



