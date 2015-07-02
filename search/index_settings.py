from django.conf import settings

SEARCH_SETTINGS = settings.SEARCH


def get_mappings():
    mappings = {}
    autocomplete_models = SEARCH_SETTINGS.get(
        'AUTOCOMPLETE_MODEL_FIELDS')

    for model_conf in autocomplete_models:
        for single_model in model_conf.get('models'):
            fields_conf = {
                "properties": {}
            }

            for field in single_model.get("fields"):
                field_mapping = {
                    "type": "string",
                    "store": True,
                    "coerce": False,
                    "index_analyzer": "autocomplete",
                    "search_analyzer": "autocomplete",
                }
                fields_conf["properties"][field] = field_mapping
            mappings[single_model.get("name").lower()] = fields_conf
    return mappings


INDEX_SETTINGS = {
    "settings": {
        "index": {
            "number_of_replicas": "1",
            "analysis": {
                "analyzer": {
                    "autocomplete": {
                        "type": "custom",
                        "filter": [
                            "standard",
                            "lowercase",
                            "stop",
                            "kstem",
                            "ngram"
                        ],
                        "tokenizer": "standard"
                    },
                    "default": {
                        "type": "snowball"
                    }
                },
                "filter": {
                    "ngram": {
                        "min_gram": "2",
                        "type": "ngram",
                        "max_gram": "15"
                    }
                }
            },
            "number_of_shards": "5",
            "version": {
                "created": "1040001"
            }
        }
    },
    "mappings": get_mappings()
}
