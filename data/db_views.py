"""
Will hold the SQL code necessary to create views in MFL v1 to aggregate
required data
"""


# Drop views so as to recreate them again ana make sure they exist
DROP_VIEWS = (
	"IF  EXISTS (SELECT * FROM sys.views WHERE object_id = OBJECT_ID(N'[dbo].[facility_owners_view]'))"
	"DROP VIEW [dbo].[facility_owners_view]"
	"GO"

	"DROP VIEW [dbo].[facility_owners_view];"
)


# links owners to their owner types
FACILITY_OWNERS_VIEW = """
CREATE VIEW [dbo].[facility_owners_view]
AS
SELECT
    dbo.lkpFacilityOwners.ownId, dbo.lkpFacilityOwners.ownName,
    dbo.lkpFacilityOwners.ownShortName, dbo.lkpFacilityOwners.ownDisplayName,
    dbo.lkpFacilityOwners.ownParent, lkpFacilityOwners_1.ownId AS parent_id,
    lkpFacilityOwners_1.ownName AS parent_name
FROM
   dbo.lkpFacilityOwners
INNER JOIN
    dbo.lkpFacilityOwners AS lkpFacilityOwners_1
ON
    dbo.lkpFacilityOwners.ownParent = lkpFacilityOwners_1.ownId
"""


__all__ = [
    DROP_VIEWS, FACILITY_OWNERS_VIEW
]
