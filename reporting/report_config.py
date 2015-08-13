REPORTS = {

    # facility county by counties
    "facility_count_by_county": {
        "filter_fields": {
            "model": "common.County",
            "filter_field_name": "ward__constituency__county",
            "return_field": ["county_name", "number_of_facilities"]
        },
        "top_level_field": "total"
    },

    # facility count by constituencies
    "facility_count_by_consituency": {
        "filter_fields": {
            "model": "common.Constituency",
            "filter_field_name": "ward__constituency",
            "return_field": ["constituency_name", "number_of_facilities"]
        },
        "top_level_field": "total"
    },

    # facility count by owner categories
    "facility_count_by_owner_category": {
        "filter_fields": {
            "model": "facilities.OwnerType",
            "filter_field_name": "owner__owner_type",
            "return_field": ["owner_category", "number_of_facilities"]
        },
        "top_level_field": "total"
    },

    # facility county by owners
    "facility_count_by_owner": {
        "filter_fields": {
            "model": "facilities.Owner",
            "filter_field_name": "owner",
            "return_field": ["owner", "number_of_facilities"]
        },
        "top_level_field": "total"
    },
    "facility_count_by_facility_type": {
        "filter_fields": {
            "model": "facilities.FacilityType",
            "filter_field_name": "facility_type",
            "return_field": ["type_category", "number_of_facilities"]
        },
        "top_level_field": "total"
    }

}
