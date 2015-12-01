from django.conf.urls import patterns, url
from haystack.views import search_view_factory

from search.query import sqs
from search.forms import PliableFacetedSearchForm
from search.views import (BetterFacetedSearchView, AutocompleteView, AnalyzerView, SearchExportView)
from cjdata.views import (IndexView, DatasetDetailView, CategoryDatasetsView,
                          StateDatasetsView, DatasetsExportView, CategoryDatasetsExportView,
                          StatesExportView)

urlpatterns = patterns(
    '',
    url(r'^export/all/$', DatasetsExportView.as_view(), name='datasets-export'),
    url(r'^export/category/(?:(?P<category>[\w-]+)/)(?:(?P<subcategory>[\w-]+)/)?$',
        CategoryDatasetsExportView.as_view(), name='datasets-by-category-export'),
    url(r'^export/location/(?P<location>[\w\s]+)/',
        StatesExportView.as_view(), name='datasets-by-location-export'),

    url(r'^data/(?P<uuid>[a-f0-9-]{32,36})/$', DatasetDetailView.as_view(), name='dataset-detail'),
    url(r'^category/(?:(?P<category>[\w-]+)/)(?:(?P<subcategory>[\w-]+)/)?$',
        CategoryDatasetsView.as_view(), name='datasets-by-category'),
    url(r'^location/(?P<location>[\w\s]+)/', StateDatasetsView.as_view(), name='datasets-by-location'),

    url(r'^search/$', search_view_factory(view_class=BetterFacetedSearchView,
                                          form_class=PliableFacetedSearchForm,
                                          searchqueryset=sqs), name='haystack_search'),
    url(r'search/export/$', SearchExportView.as_view(), name='search_export'),
    url(r'^search/analyze/', AnalyzerView.as_view(), name='search_analyze'),
    url(r'^autocomplete/$', AutocompleteView.as_view(), name='haystack_autocomplete'),
    url(r'^$', IndexView.as_view(), name='index')
)
