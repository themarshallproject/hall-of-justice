from haystack.views import FacetedSearchView
from haystack.generic_views import SearchMixin
from haystack.query import SearchQuerySet
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from search.forms import PliableFacetedSearchForm
from cjdata.models import Dataset
from common.utils import generate_csv
from django.http import StreamingHttpResponse


import collections

basestring = (str, bytes)


class BetterFacetedSearchView(FacetedSearchView):

    def extra_context(self):
        extra = super(BetterFacetedSearchView, self).extra_context()

        if self.form.selected_facets:
            selected_facets = [(k.replace('_exact', ''), v) for k, v in (item.split(':') for item in self.form.selected_facets)]
            extra['selected_facets'] = dict(selected_facets)

        return extra


class AutocompleteView(View):
    """provides autocompletion JSON endpoint"""

    def get(self, request, *args, **kwargs):
        def flatten(l):
            for el in l:
                if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
                    for sub in flatten(el):
                        yield sub
                else:
                    yield el
        query = request.GET.get('q', '').lower()
        sqs = SearchQuerySet().using('autocomplete').filter(content=query)

        # texts = ((t for t in s) if not s.__hash__ else s.text for s in sqs)
        texts = flatten((s.text for s in sqs))
        lower_texts = (t.lower() for t in texts)
        suggestions = ({'value': p.title()} for p in set(lower_texts) if query.lower() in p.lower())

        return JsonResponse({'results': list(suggestions)[:100]})


class AnalyzerView(TemplateView):
    '''Provides a view to show how an analzyer transforms a search string into tokens'''

    template_name = 'search/analyzer_result.html'

    def get_context_data(self, **kwargs):
        context = super(AnalyzerView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()

        context['query'] = query

        sqs = SearchQuerySet().using('default')
        token_dict = sqs.query.backend.analyze_text(query, analyzer='cjdata_analyzer')

        tokens = token_dict.get('tokens', None)
        for tok in tokens:
            # Use offsets to pair token with original text
            start_offset = tok.get('start_offset', -1)
            end_offset = tok.get('end_offset', -1)
            if start_offset > -1 and end_offset > -1:
                tok['original_string'] = query[int(start_offset):int(end_offset)]

        context['tokens'] = tokens

        return context


class SearchExportView(View, SearchMixin):
    """docstring for SeachExportView"""
    form_class = PliableFacetedSearchForm
    http_method_names = ['get']
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        sqs = form.search()
        result_objects = (result.object for result in sqs)

        output_fieldnames = [f.name for f in Dataset._meta.get_fields() if f.name != 'id']
        csv_data = generate_csv(result_objects, output_fieldnames)

        response = StreamingHttpResponse(csv_data, content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="criminal-justice-{}-rows.csv"'.format(sqs.count())
        return response

    # def form_valid(self, form):
    #     return super(SearchExportView, self).form_valid()

    # def form_invalid(self, form):
    #     # do something -- log the error, etc -- if needed
    #     return super(SearchExportView, self).form_invalid()
