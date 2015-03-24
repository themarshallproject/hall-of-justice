# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import warnings

from django.conf import settings

import haystack
from haystack.backends.elasticsearch_backend import ElasticsearchSearchEngine
from haystack.constants import DJANGO_CT
from haystack.exceptions import MissingDependency
from haystack.utils import get_model_ct
from elasticstack.backends import ConfigurableElasticBackend

try:
    import elasticsearch
except ImportError:
    raise MissingDependency("The 'elasticsearch' backend requires the installation of 'elasticsearch'. Please refer to the documentation.")


class SimpleESBackend(ConfigurableElasticBackend):
    """An attempt at a custom simple ES search using simpler query syntax."""

    def build_search_kwargs(self, query_string, sort_by=None, start_offset=0, end_offset=None,
                            fields='', highlight=False, facets=None,
                            date_facets=None, query_facets=None,
                            narrow_queries=None, spelling_query=None,
                            within=None, dwithin=None, distance_point=None,
                            models=None, limit_to_registered_models=None,
                            result_class=None):
        index = haystack.connections[self.connection_alias].get_unified_index()
        content_field = index.document_field

        if query_string == '*:*':
            kwargs = {
                'query': {
                    "match_all": {},
                    'analyzer': self.DEFAULT_ANALYZER  # setting courtesy of ConfigurableElasticBackend
                },
            }
        else:
            kwargs = {
                'query': {
                    'match': {
                        str(content_field): {
                            'query': query_string,
                            'analyzer': self.DEFAULT_ANALYZER  # setting courtesy of ConfigurableElasticBackend
                        }
                    },
                },
            }

        # so far, no filters
        filters = []

        if fields:
            if isinstance(fields, (list, set)):
                fields = " ".join(fields)

            kwargs['fields'] = fields

        if sort_by is not None:
            order_list = []
            for field, direction in sort_by:
                if field == 'distance' and distance_point:
                    # Do the geo-enabled sort.
                    lng, lat = distance_point['point'].get_coords()
                    sort_kwargs = {
                        "_geo_distance": {
                            distance_point['field']: [lng, lat],
                            "order": direction,
                            "unit": "km"
                        }
                    }
                else:
                    if field == 'distance':
                        warnings.warn("In order to sort by distance, you must call the '.distance(...)' method.")

                    # Regular sorting.
                    sort_kwargs = {field: {'order': direction}}

                order_list.append(sort_kwargs)

            kwargs['sort'] = order_list

        # From/size offsets don't seem to work right in Elasticsearch's DSL. :/
        # if start_offset is not None:
        #     kwargs['from'] = start_offset

        # if end_offset is not None:
        #     kwargs['size'] = end_offset - start_offset

        if highlight is True:
            kwargs['highlight'] = {
                'fields': {
                    content_field: {'store': 'yes'},
                }
            }

        if self.include_spelling:
            kwargs['suggest'] = {
                'suggest': {
                    'text': spelling_query or query_string,
                    'term': {
                        # Using content_field here will result in suggestions of stemmed words.
                        'field': '_all',
                    },
                },
            }

        if narrow_queries is None:
            narrow_queries = set()

        if facets is not None:
            kwargs.setdefault('facets', {})

            for facet_fieldname, extra_options in facets.items():
                facet_options = {
                    'terms': {
                        'field': facet_fieldname,
                        'size': 100,
                    },
                }
                # Special cases for options applied at the facet level (not the terms level).
                if extra_options.pop('global_scope', False):
                    # Renamed "global_scope" since "global" is a python keyword.
                    facet_options['global'] = True
                if 'facet_filter' in extra_options:
                    facet_options['facet_filter'] = extra_options.pop('facet_filter')
                facet_options['terms'].update(extra_options)
                kwargs['facets'][facet_fieldname] = facet_options

        if date_facets is not None:
            kwargs.setdefault('facets', {})

            for facet_fieldname, value in date_facets.items():
                # Need to detect on gap_by & only add amount if it's more than one.
                interval = value.get('gap_by').lower()

                # Need to detect on amount (can't be applied on months or years).
                if value.get('gap_amount', 1) != 1 and interval not in ('month', 'year'):
                    # Just the first character is valid for use.
                    interval = "%s%s" % (value['gap_amount'], interval[:1])

                kwargs['facets'][facet_fieldname] = {
                    'date_histogram': {
                        'field': facet_fieldname,
                        'interval': interval,
                    },
                    'facet_filter': {
                        "range": {
                            facet_fieldname: {
                                'from': self._from_python(value.get('start_date')),
                                'to': self._from_python(value.get('end_date')),
                            }
                        }
                    }
                }

        if query_facets is not None:
            kwargs.setdefault('facets', {})

            for facet_fieldname, value in query_facets:
                kwargs['facets'][facet_fieldname] = {
                    'query': {
                        'match': {
                            'query': value,
                        }
                    },
                }

        if limit_to_registered_models is None:
            limit_to_registered_models = getattr(settings, 'HAYSTACK_LIMIT_TO_REGISTERED_MODELS', True)

        if models and len(models):
            model_choices = sorted(get_model_ct(model) for model in models)
        elif limit_to_registered_models:
            # Using narrow queries, limit the results to only models handled
            # with the current routers.
            model_choices = self.build_models_list()
        else:
            model_choices = []

        if len(model_choices) > 0:
            filters.append({"terms": {DJANGO_CT: model_choices}})

        for q in narrow_queries:
            filters.append({
                'fquery': {
                    'query': {
                        'query_string': {
                            'query': q
                        },
                    },
                    '_cache': True,
                }
            })

        if within is not None:
            from haystack.utils.geo import generate_bounding_box

            ((south, west), (north, east)) = generate_bounding_box(within['point_1'], within['point_2'])
            within_filter = {
                "geo_bounding_box": {
                    within['field']: {
                        "top_left": {
                            "lat": north,
                            "lon": west
                        },
                        "bottom_right": {
                            "lat": south,
                            "lon": east
                        }
                    }
                },
            }
            filters.append(within_filter)

        if dwithin is not None:
            lng, lat = dwithin['point'].get_coords()

            # NB: the 1.0.0 release of elasticsearch introduce an
            #     incompatible change on the distance filter formating
            if elasticsearch.VERSION >= (1, 0, 0):
                distance = "%(dist).6f%(unit)s" % {
                        'dist': dwithin['distance'].km,
                        'unit': "km"
                    }
            else:
                distance = dwithin['distance'].km

            dwithin_filter = {
                "geo_distance": {
                    "distance": distance,
                    dwithin['field']: {
                        "lat": lat,
                        "lon": lng
                    }
                }
            }
            filters.append(dwithin_filter)

        # if we want to filter, change the query type to filteres
        if filters:
            kwargs["query"] = {"filtered": {"query": kwargs.pop("query")}}
            if len(filters) == 1:
                kwargs['query']['filtered']["filter"] = filters[0]
            else:
                kwargs['query']['filtered']["filter"] = {"bool": {"must": filters}}

        return kwargs


class SimpleESSearchEngine(ElasticsearchSearchEngine):
    backend = SimpleESBackend
