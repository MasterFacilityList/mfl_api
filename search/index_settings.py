INDEX_SETTINGS = {
    "settings": {
        "index": {
            "creation_date": "1434101603851",
            "uuid": "HHzIptOYTxOowFCIxY7_eA",
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
                        "min_gram": "4",
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
    "mappings": {
        "facility": {
            "properties": {
                "name": {
                    "type": "string",
                    "index_analyzer": "autocomplete",
                    "search_analyzer": "snowball"
                }
            }
        }
    }
}
