Workflow
==========
MFL API v2 is a liberally licensed ( `MIT`_ license ) project. All development
occurs in the open on the `MFL API Github project`_. We use the
`MFL API Github issue list`_ to manage bug reports and enhancement requests.

.. _`MIT`: http://choosealicense.com/licenses/mit/
.. _`MFL API Github project`: https://github.com/MasterFacilityList/mfl_api
.. _`MFL API Github issue list`: https://github.com/MasterFacilityList/mfl_api/issues

This project uses the `GitFlow Workflow`_.

 .. _`GitFlow Workflow`: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

In summary:

 * all work should occur in feature branches
 * the target for pull requests is the ``develop`` branch
 * the release manager ( presently `@ngurenyaga <https://github.com/ngurenyaga>`_ ) will periodically create release branches that ultimately get merged into ``master`` and tagged
 * fixes on released versions will occur in hotfix branches

We adhere to semantic versioning - https://semver.org .

In order to deploy a new version, you will need to have a ``$HOME/.pypirc``
that has the correct pypi credentials. The command to deploy is ``fab deploy``.
The credentials are not stored on GitHub - for obvious reasons.


.. toctree::
    :maxdepth: 2
