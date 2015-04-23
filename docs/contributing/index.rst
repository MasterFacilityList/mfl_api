Contributing
==============
TBD - **everything here is work in progress**

Contributing
-------------
This project uses the ``git-flow`` workflow. You can find more information
by following the links at https://github.com/nvie/gitflow .

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

    workflow
    code_of_conduct
