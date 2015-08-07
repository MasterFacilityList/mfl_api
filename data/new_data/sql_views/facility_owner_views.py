
FACILITY_OWNERS_VIEW = """
CREATE VIEW [dbo].[facility_owners_view]
AS
SELECT     dbo.lkpFacilityOwners.ownId, dbo.lkpFacilityOwners.ownName, dbo.lkpFacilityOwners.ownShortName, dbo.lkpFacilityOwners.ownDisplayName, 
                      dbo.lkpFacilityOwners.ownParent, lkpFacilityOwners_1.ownId AS parent_id, lkpFacilityOwners_1.ownName AS parent_name
FROM         dbo.lkpFacilityOwners INNER JOIN
                      dbo.lkpFacilityOwners AS lkpFacilityOwners_1 ON dbo.lkpFacilityOwners.ownParent = lkpFacilityOwners_1.ownId

GO
"""
