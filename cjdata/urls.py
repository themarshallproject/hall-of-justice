from django.conf.urls import patterns, url
from haystack.forms import FacetedSearchForm
from haystack.views import search_view_factory

from cjdata.search.query import sqs
from cjdata.search.views import BetterFacetedSearchView
from cjdata.views import DatasetDetailView

urlpatterns = patterns(
    '',
    url(r'^data/(?P<uuid>[a-f0-9-]{32,36})/$', DatasetDetailView.as_view(), name='dataset-detail'),
    url(r'^$', search_view_factory(view_class=BetterFacetedSearchView,
                                   form_class=FacetedSearchForm,
                                   searchqueryset=sqs), name='haystack_search'),
)
