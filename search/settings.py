from cjdata.models import STATE_NATL_LOOKUP

STATES_SYNONYMS = ["{}=>{}".format(v.lower(), k.lower()) for k, v in STATE_NATL_LOOKUP.items()]

'''
In order to make multi-word synonyms compatible with the synonym filter,
we must map multi-word phrases to tokens without spaces, like "shu" or "stopandfrisk".
'''

cj_synonyms = [
    "homicide,murder,kill",
    "close management,shu,solitary,solitary housing unit,solitary confinement=>shu",
    "stop frisk,terry stop,pedestrian stop,stops,stop search,stop question frisk=>stopandfrisk",
    "death penalty,capital punishment=>deathpenalty",
    "deconfliction,information sharing=>deconfliction",
    "arrests,bookings",
    "public legal services,indigent defense,public defenders=>publicdefenders",
    "calls service,calls assistance,CAD,911 call,CFS,dispatch=>911call",
    "domestic violence,intimate partner violence,domestic abuse,dating violence=>domesticviolence",
    "use force,officer-involved shooting,death custody,arrest-related death=>useofforce",
    "larceny,theft",
    "prison,jail",
    "exoneration,pardon,dismissal",
    "restitution,victim compensation,compensation=>restitution",
    # "juvenile delinquent,juvenile,delinquent=>juvenile",
    "parole,probation",
    "part 1 crime,part one crime,index crime=>part1crime",
    "k9,canine=>dog"
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
