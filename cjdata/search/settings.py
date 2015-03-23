from cjdata.models import STATE_NATL_LOOKUP

STATES_SYNONYMS = ["{}=>{}".format(v.lower(), k.lower()) for k, v in STATE_NATL_LOOKUP.items()]

cj_synonyms = [
    "homicide,murder,kill",
    "close management,shu,solitary housing unit,solitary,solitary confinement=>shu",
    "stop and frisk,Terry stop,pedestrian stop,stops,stop and search,stop question and frisk",
    "death penalty,capital punishment",
    "deconfliction,information sharing"
    "arrests,bookings",
    "public legal services,indigent defense,public defenders",
    "calls for service,calls for assistance,CAD,911 calls,CFS,dispatch",
    "domestic violence,intimate partner violence,domestic abuse,dating violence",
    "use of force,officer-involved shooting,death in custody,arrest-related death"
    "larceny,theft",
    "prison,jail",
    "exoneration,pardon,dismissal",
    "restitution,victim compensation,compensation",
    "juvenile delinquent,juvenile,delinquent",
    "parole,probation",
    "Part I crime,Index crime"
]
cj_synonyms.extend(STATES_SYNONYMS)

DATASET_INDEX_SETTINGS = {
    "settings": {
        "analysis": {
            "filter": {
                "cjdata_synonym_filter": {
                    "type": "synonym",
                    "synonyms": cj_synonyms
                },
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english"
                }
            },
            "analyzer": {
                "cjdata_analyzer": {
                    "tokenizer": "classic",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "cjdata_synonym_filter",
                        "english_possessive_stemmer",
                        "english_stemmer",
                    ]
                }
            }
        }
    }
}
