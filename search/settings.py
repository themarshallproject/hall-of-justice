from cjdata.models import STATE_NATL_LOOKUP

STATES_SYNONYMS = ["{}=>{}".format(v.lower(), k.lower()) for k, v in STATE_NATL_LOOKUP.items()]

CASE_SENSITVE_SYNONYMS = [
    'CFS,CAD=>call_for_service',
    'STOP,STOP Violence=>domestic_violence'
]

CJ_SYNONYMS = [
    "homicide,murder,kill",
    "close management,solitary housing unit,special housing unit,solitary confinement,shu,solitary=>solitary_confinement",
    "stop frisk,terry stop,pedestrian stop,stop search,stop question frisk=>terry_stop",
    "death penalty,capital punishment",
    "deconfliction,information sharing",
    "arrests,bookings",
    "public legal services,indigent defense,public defenders",
    "calls service,calls assistance,911 call,dispatc,call_for_serviceh=>call_for_service",
    "domestic violence,intimate partner violence,domestic abuse,dating violence,domestic_violence=>domestic_violence",
    "use force,officer-involved shooting,death custody,arrest-related death",
    "larceny,theft",
    "prison,jail",
    "exoneration,pardon,dismissal",
    "restitution,victim compensation,compensation",
    "juvenile delinquent,juvenile,delinquent",
    "parole,probation",
    "part 1 crime,index crime=>index_crime",
    "k9,canine=>dog"
]
CJ_SYNONYMS.extend(STATES_SYNONYMS)

DATASET_INDEX_SETTINGS = {
    "settings": {
        "analysis": {
            "filter": {
                "case_sensitive_filter": {
                    "type": "synonym",
                    "synonyms": CASE_SENSITVE_SYNONYMS
                },
                "cjdata_synonym_filter": {
                    "type": "synonym",
                    "synonyms": CJ_SYNONYMS
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
                },
                "haystack_edgengram": {
                    "type": "edgeNGram",
                    "min_gram": 2,
                    "max_gram": 15
                }
            },
            "analyzer": {
                "cjdata_analyzer": {
                    "tokenizer": "classic",
                    "filter": [
                        "case_sensitive_filter",
                        "lowercase",
                        "english_stop",
                        "cjdata_synonym_filter",
                        "english_possessive_stemmer",
                        "english_stemmer",
                    ]
                },
                "edgengram_analyzer": {
                    "type": "custom",
                    "tokenizer": "lowercase",
                    "filter": ["haystack_edgengram"]
                }
            }
        }
    }
}
