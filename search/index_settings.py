INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 1,
        "index.mapping.ignore_malformed": False,
        "index.mapping.coerce": False,
        "index.mapper.dynamic": False,
        "analysis": {
            "filter": {
                "autocomplete_filter": {
                    "type": "edge_ngram",
                    "min_gram": 3,
                    "max_gram": 20
                },
                "synonym": {
                    "type": "synonym",
                    "synonyms": ["sneakers", "endebess"]
                }
            },
            "analyzer": {
                "autocomplete": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "standard",
                        "lowercase",
                        "stop",
                        "autocomplete_filter"
                    ]
                },
                "standard_with_stopwords": {
                    "type": "standard",
                    "stopwords": []
                },
                "synonyms": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "standard",
                        "lowercase",
                        "stop",
                        "synonym"
                    ]
                }
            }
        }
    },
    "mappings": {
        "facility": {
            "dynamic": "strict",
            "properties": {
                "name": {
                    "type": "string",
                    "index": "analyzed",
                    "store": True,
                    "index_analyzer": "standard_with_stopwords",
                    "search_analyzer": "standard_with_stopwords"
                },
                "name_autocomplete": {
                    "type": "string",
                    "index": "analyzed",
                    "store": True,
                    "index_analyzer": "autocomplete",
                    "search_analyzer": "standard_with_stopwords"
                }
            }
        }
    }
}
