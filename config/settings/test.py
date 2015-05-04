from .base import *  # NOQA


if os.getenv('CI') == 'true':
    SEARCH = {
        "ELASTIC_URL": "http://127.0.0.1:9200/",
        "INDEX_NAME": "mfl_index"
    }
