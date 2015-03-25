from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet
from django.views.generic import View
from django.http import JsonResponse


class BetterFacetedSearchView(FacetedSearchView):

    def extra_context(self):
        extra = super(BetterFacetedSearchView, self).extra_context()

        if self.form.selected_facets:
            selected_facets = [(k.replace('_exact', ''), v) for k, v in (item.split(':') for item in self.form.selected_facets)]
            extra['selected_facets'] = dict(selected_facets)

        return extra


class AutocompleteView(View):
    """provides autocompletion JSON endpoint"""

    def get(self, request):
        query = request.GET.get('q', '')
        sqs = SearchQuerySet().using('autocomplete').filter(content=query)

        suggestions = set([s.path for s in sqs])

        response = JsonResponse({'results': list(suggestions)})

        return response
