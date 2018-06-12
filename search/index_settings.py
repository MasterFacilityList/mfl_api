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
                    "search_analyzer": "autocomplete"
                }
                fields_conf["properties"][field] = field_mapping
            mappings[single_model.get("name").lower()] = fields_conf
    return mappings


MAPPING = get_mappings()
MAPPING["doc"] = {
    "properties": {
        "text": {
            "type": "string",
            "index_options": "docs"
        }
    }
}


STOP_WORDS = SEARCH_SETTINGS.get("STOP_WORDS")


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
                            "edgeNGram"
                        ],
                        "tokenizer": "standard"
                    },
                    "default": {
                        "type": "snowball",
                        "stopwords": STOP_WORDS
                    }
                },
                "filter": {
                    "edgeNGram": {
                        "min_gram": "2",
                        "type": "edgeNGram",
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
    "mappings": MAPPING
}
