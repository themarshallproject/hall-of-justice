# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from haystack.backends.elasticsearch_backend import ElasticsearchSearchEngine
from elasticstack.backends import ConfigurableElasticBackend


class SimpleESBackend(ConfigurableElasticBackend):
    """An attempt at a custom simple ES search using simpler query syntax that supports AND, OR, etc."""
    RESERVED_WORDS = ['TO']


class SimpleESSearchEngine(ElasticsearchSearchEngine):
    backend = SimpleESBackend
