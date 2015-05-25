INDEX_SETTINGS = {
    "settings": {
        "analysis": {
            "analyzer": {
                "default": {
                    "type": "snowball",
                    "search": "snowball"

                },
                "mfl_analyzer": {
                    "type": "snowball",
                    "language": "English"
                }
            }
        }
    }
}
