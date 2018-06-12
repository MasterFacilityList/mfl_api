Deploying to PyPI
===================

You will need to have a `$HOME/.pypirc` file similar to this example:


    [distutils]
    index-servers =
        pypi

    [pypi]
    repository = https://pypi.python.org/pypi
    username: <your pypi username>
    password: <your pypi password>

With that in place, `fab deploy` should send the package to the cheese
shop.

You can obtain a username and password by running
`python setup.py register` in the project home ( the same folder that
has the `setup.py` ).
