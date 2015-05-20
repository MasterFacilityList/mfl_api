INDEX_SETTINGS = {
    "settings": {
        "analysis": {
            "analyzer": {
                "synonym_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["synonym", "unique_stem"]
                },
                "ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "lowercase",
                    "filter": ["mfl_ngram", "synonym", "unique_stem"]
                },
                "edgengram_analyzer": {
                    "type": "custom",
                    "tokenizer": "lowercase",
                    "filter": ["mfl_edgengram", "unique_stem"]
                }
            },
            "tokenizer": {
                "mfl_ngram_tokenizer": {
                    "type": "nGram",
                    "min_gram": 3,
                    "max_gram": 15,
                },
                "mfl_edgengram_tokenizer": {
                    "type": "edgeNGram",
                    "min_gram": 2,
                    "max_gram": 15,
                    "side": "front"
                }
            },
            "filter": {
                "mfl_ngram": {
                    "type": "nGram",
                    "min_gram": 3,
                    "max_gram": 15
                },
                "mfl_edgengram": {
                    "type": "edgeNGram",
                    "min_gram": 2,
                    "max_gram": 15
                },
                "synonym": {
                    "type": "synonym",
                    "ignore_case": "true",
                    "synonyms_path": "synonyms.txt"
                },

                "unique_stem": {
                    "type": "unique",
                    "only_on_same_position": True
                }
            },
            "mappings": {
                "facility": {
                    "properties": {
                        "name": {
                            "type": "string",
                            "analyzer": "edgengram_analyzer"
                        },
                        "location_dec": {
                            "type": "synonym_analyzer"
                        }
                    }
                },
                "owner": {
                    "properties": {
                        "name": {
                            "type": "string",
                            "analyzer": "edgengram_analyzer"
                        }
                    }
                }
            }

        }
    }
}


#  Enable suggestions
# Add auto complete
# add synonyms
# enable query
