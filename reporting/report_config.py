"""Module holding the configuration of various reports"""


REPORTS = {

    # facility county by counties
    "facility_count_by_county": {
        "type": "simple",
        "filter_fields": {
            "model": "common.County",
            "filter_field_name": "ward__constituency__county",
            "return_field": ["county_name", "number_of_facilities"]
        },
        "top_level_field": "total"
    },

    # facility count by constituencies
    "facility_count_by_consituency": {
        "type": "simple",
        "filter_fields": {
            "model": "common.Constituency",
            "filter_field_name": "ward__constituency",
            "return_field": ["constituency_name", "number_of_facilities"]
        },
        "extra_filters": {
            "county": {
                "path": "common.County",
                "filter_field_name": "ward__constituency__county"
            }

        },
        "top_level_field": "total"
    },

    # facility count by owner categories
    "facility_count_by_owner_category": {
        "type": "simple",
        "filter_fields": {
            "model": "facilities.OwnerType",
            "filter_field_name": "owner__owner_type",
            "return_field": ["owner_category", "number_of_facilities"]
        },
        "top_level_field": "total"
    },

    # facility count by owners
    "facility_count_by_owner": {
        "type": "simple",
        "filter_fields": {
            "model": "facilities.Owner",
            "filter_field_name": "owner",
            "return_field": ["owner", "number_of_facilities"]
        },
        "extra_filters": {
            "owner_type": {
                "path": "facilities.OwnerType",
                "filter_field_name": "owner__owner_type"
            }
        },
        "top_level_field": "total"
    },


    # facility county by facility types
    "facility_count_by_facility_type": {
        "type": "simple",
        "filter_fields": {
            "model": "facilities.FacilityType",
            "filter_field_name": "facility_type",
            "return_field": ["type_category", "number_of_facilities"]
        },
        "extra_filters": {
            "owner_type": {
                "path": "facilities.OwnerType",
                "filter_field_name": "owner__owner_type"
            }
        },
        "top_level_field": "total"
    },
    "facility_count_by_facility_type_detailed": {
        "type": "complex",
        "filter_fields": {
            "model": "facilities.FacilityType",
            "filter_field_name": "facility_type",
            "return_field": ["type_category", "number_of_facilities"]
        },
        "extra_filters": {
            "owner_type": {
                "path": "facilities.OwnerType",
                "filter_field_name": "owner__owner_type"
            }
        },
        "facility_fields": [
            {
                "name": "county",
                "field_name": "ward.constituency.county.name"
            },
            {
                "name": "owner_category",
                "field_name": "owner.owner_type.name"
            }
        ],
        "group_by": {
            "path": "common.County",
            "name": "county",
            "field_name": "ward__constituency__county"
        },
        "top_level_field": "total"
    }

}
