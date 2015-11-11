
CREATE MATERIALIZED VIEW mfl_gis_drilldown AS
 SELECT st_x(mfl_gis_facilitycoordinates.coordinates) AS lat,
    st_y(mfl_gis_facilitycoordinates.coordinates) AS lng,
    facilities_facility.name,
    common_county.code AS county,
    common_constituency.code AS constituency,
    common_ward.code AS ward
   FROM ((((mfl_gis_facilitycoordinates
     JOIN facilities_facility ON ((mfl_gis_facilitycoordinates.facility_id = facilities_facility.id)))
     JOIN common_ward ON ((facilities_facility.ward_id = common_ward.id)))
     JOIN common_constituency ON ((common_ward.constituency_id = common_constituency.id)))
     JOIN common_county ON ((common_constituency.county_id = common_county.id)))
  WHERE ((((((mfl_gis_facilitycoordinates.deleted = false) AND (facilities_facility.is_published = true)) AND (facilities_facility.rejected = false)) AND (facilities_facility.is_classified = false)) AND (facilities_facility.closed = false)) AND (facilities_facility.approved = true))
  ORDER BY mfl_gis_facilitycoordinates.updated DESC, mfl_gis_facilitycoordinates.created DESC;
