from django.conf.urls import patterns, url
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView, search_view_factory

from cjdata.views import DatasetDetailView

sqs = SearchQuerySet().facet('states').facet('group_name').facet('tags')

urlpatterns = patterns(
    '',
    url(r'^data/(?P<uuid>[a-f0-9-]{32,36})/$', DatasetDetailView.as_view(), name='dataset-detail'),
)

urlpatterns += patterns(
    'haystack.views',
    url(r'^$', search_view_factory(view_class=FacetedSearchView,
                                   form_class=FacetedSearchForm,
                                   searchqueryset=sqs), name='haystack_search'),
)
