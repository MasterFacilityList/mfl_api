def get_version(v):
    """
    Generate a PEP386  compliant version

    Stolen from django.utils.version.get_version

    :param v tuple: A five part tuple indicating the version
    :returns str: Compliant version
    """
    assert isinstance(v, tuple)
    assert len(v) == 5
    assert v[3] in ('alpha', 'beta', 'rc', 'final')

    parts = 2 if v[2] == 0 else 3
    main = '.'.join(str(i) for i in v[:parts])
    sub = ''
    if v[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[v[3]] + str(v[4])
    return str(main + sub)

VERSION = (2, 0, 0, 'alpha', 8)

__version__ = get_version(VERSION)

try:
    from settings import *  # noqa
except ImportError:  # Will occur on first install
    pass  # NOQA
