INDEX_SETTINGS = {
    "settings": {
        "analysis": {
            "analyzer": {
                "synonym_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["synonym"]
                },
                "ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "lowercase",
                    "filter": ["mfl_ngram", "synonym"]
                },
                "edgengram_analyzer": {
                    "type": "custom",
                    "tokenizer": "lowercase",
                    "filter": ["mfl_edgengram"]
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
                }
            }
        }
    }
}
