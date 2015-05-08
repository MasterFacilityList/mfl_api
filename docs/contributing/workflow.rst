Workflow
==========
This project uses the `GitFlow Workflow`_.

 .. _`GitFlow Workflow`: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

In summary:

 * all work should occur in feature branches
 * the target for pull requests is the ``develop`` branch
 * the release manager ( presently @ngurenyaga ) will periodically create release branches that ultimately get merged into ``master`` and tagged
 * fixes on released versions will occur in hotfix branches

We adhere to semantic versioning - https://semver.org .

In order to deploy a new version, you will need to have a ``$HOME/.pypirc``
that has the correct pypi credentials. The command to deploy is ``fab deploy``.
The credentials are not stored on GitHub - for obvious reasons.


.. toctree::
    :maxdepth: 2
