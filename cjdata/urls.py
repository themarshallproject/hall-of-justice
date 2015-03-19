from django.conf.urls import patterns, url
from haystack.forms import FacetedSearchForm
from haystack.views import FacetedSearchView, search_view_factory

from cjdata.search import sqs
from cjdata.views import DatasetDetailView

urlpatterns = patterns(
    '',
    url(r'^data/(?P<uuid>[a-f0-9-]{32,36})/$', DatasetDetailView.as_view(), name='dataset-detail'),
    url(r'^$', search_view_factory(view_class=FacetedSearchView,
                                   form_class=FacetedSearchForm,
                                   searchqueryset=sqs), name='haystack_search'),
)
