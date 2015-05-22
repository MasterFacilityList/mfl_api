INDEX_SETTINGS = {
    "settings": {"number_of_shards": 1},
    "mappings": {
        "facility": {
            "properties": {
                "name": {
                    "type": "string",
                    "analyzer": "english",
                    "fields": {
                        "std": {
                            "type": "string",
                            "analyzer": "standard"
                        }
                    }
                }
            }
        }
    }
}
