from haystack.forms import (SearchForm, FacetedSearchForm)
from haystack.inputs import Raw
from django import forms


class PliableSearchForm(SearchForm):
    parse_query = forms.BooleanField(required=False)

    '''Adapted from FacetedSearchForm, but it performs a clean_query, not an auto_query'''

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        if self.cleaned_data.get('parse_query', False):
            sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])
        else:
            sqs = self.searchqueryset.raw_search(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs


class PliableFacetedSearchForm(FacetedSearchForm, PliableSearchForm):

    '''Adapted from FacetedSearchForm, but it performs a clean_query, not an auto_query'''

    def search(self):
        sqs = super(FacetedSearchForm, self).search()

        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value:
                sqs = sqs.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))

        return sqs

