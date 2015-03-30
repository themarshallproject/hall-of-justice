from django.conf.urls import patterns, url
from haystack.forms import FacetedSearchForm
from haystack.views import search_view_factory

from cjdata.search.query import sqs
from cjdata.search.views import (BetterFacetedSearchView, AutocompleteView,)
from cjdata.views import (DatasetDetailView, CategoryDatasetsView)

urlpatterns = patterns(
    '',
    url(r'^data/(?P<uuid>[a-f0-9-]{32,36})/$', DatasetDetailView.as_view(), name='dataset-detail'),
    url(r'^category/(?P<path>[\w/-]+)/$', CategoryDatasetsView.as_view(), name='dataset-list'),
    url(r'^$', search_view_factory(view_class=BetterFacetedSearchView,
                                   form_class=FacetedSearchForm,
                                   searchqueryset=sqs), name='haystack_search'),
    url(r'^autocomplete/$', AutocompleteView.as_view(), name='haystack_autocomplete'),
)
