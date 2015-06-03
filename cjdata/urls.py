from django.conf.urls import patterns, url
from haystack.forms import FacetedSearchForm
from haystack.views import search_view_factory

from search.query import sqs
from search.views import (BetterFacetedSearchView, AutocompleteView,)
from cjdata.views import (IndexView, DatasetDetailView, CategoryDatasetsView, StateDatasetsView)

urlpatterns = patterns(
    '',
    url(r'^data/(?P<uuid>[a-f0-9-]{32,36})/$', DatasetDetailView.as_view(), name='dataset-detail'),
    url(r'^category/(?:(?P<category>[\w-]+)/)(?:(?P<subcategory>[\w-]+)/)?$',
        CategoryDatasetsView.as_view(), name='datasets-by-category'),
    url(r'^location/(?P<location>[\w\s]+)/', StateDatasetsView.as_view(), name='datasets-by-location'),
    url(r'^search/$', search_view_factory(view_class=BetterFacetedSearchView,
                                          form_class=FacetedSearchForm,
                                          searchqueryset=sqs), name='haystack_search'),
    url(r'^autocomplete/$', AutocompleteView.as_view(), name='haystack_autocomplete'),
    url(r'^$', IndexView.as_view(), name='index')
)
