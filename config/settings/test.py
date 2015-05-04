from .base import *  # NOQA


if os.getenv('CI') == 'true':
    SEARCH = {
        "ELASTIC_URL": "http://circlehost:9200/",
        "INDEX_NAME": "mfl_index"
    }
