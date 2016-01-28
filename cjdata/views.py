from django.views.generic import View, DetailView, ListView, TemplateView
from django.shortcuts import get_object_or_404
from cjdata.models import Dataset, Category, STATE_NATL_LOOKUP
from search.query import sqs
from common.views import CSVExportMixin
from django.db.models import Q
import itertools
from collections import Counter


class IndexView(TemplateView):
    template_name = "cjdata/index.html"


class DatasetDetailView(DetailView):
    model = Dataset
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super(DatasetDetailView, self).get_context_data(**kwargs)
        context['more_like_this'] = sqs.more_like_this(self.object)[:100]
        return context


class DatasetsView(ListView):

    def complete_query(self, query):
        # filter query based on selected_facets GET parameters
        if self.request.GET.getlist('selected_facets', False):
            self.selected_facets = dict([(k.replace('_exact', ''), v) for k, v in (item.split(':') for item in self.request.GET.getlist('selected_facets'))])
        else:
            self.selected_facets = {}

        for k, v in self.selected_facets.items():
            if k in ['states', 'sectors']:
                query = query & Q(**{k+'__contained_by': [v]})
            else:
                query = query & Q(**{k: v})

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # counter number of each states, sectors, group_name, and access_type
        obj_list = self.object_list
        context['states'] = Counter([val for sublist in [x.states for x in obj_list] for val in sublist]).items()
        context['sectors'] = Counter([val for sublist in [x.sectors for x in obj_list] for val in sublist]).items()
        context['group_name'] = Counter([x.group_name for x in obj_list]).items()
        context['access_type'] = Counter([x.access_type for x in obj_list]).items()
        context['selected_facets'] = self.selected_facets

        return context


class CategoryDatasetsView(DatasetsView):
    model = Dataset
    paginate_by = 50

    def get_queryset(self):

        cat_slug = self.kwargs.get('category', None)
        subcat_slug = self.kwargs.get('subcategory', None)
        if cat_slug != 'none':
            self.category = get_object_or_404(Category, slug=cat_slug, parent__isnull=True)
            if subcat_slug:
                self.category = get_object_or_404(Category, slug=subcat_slug, parent=self.category)
                query = Q(categories=self.category)
            else:
                query = (Q(categories=self.category) | Q(categories__parent=self.category))
        else:
            query = Q(categories__isnull=True)

        return Dataset.objects.filter(super().complete_query(query))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = getattr(self, 'category', None)
        return context


class StateDatasetsView(DatasetsView):
    model = Dataset
    paginate_by = 50

    def get_queryset(self):
        self.state_abbr = self.kwargs.get('location', '').upper()
        query = Q(states__contains=[self.state_abbr])
        return Dataset.objects.filter(super().complete_query(query))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location_abbr'] = self.state_abbr
        context['location'] = STATE_NATL_LOOKUP.get(self.state_abbr, None)
        return context


class StatesExportView(CSVExportMixin, StateDatasetsView):
    paginate_by = None


class DatasetsExportView(CSVExportMixin, View):
    model = Dataset

    def get_queryset(self):
        queryset = super(DatasetsExportView, self).get_queryset()
        queryset = queryset.prefetch_related('categories')
        return queryset


class CategoryDatasetsExportView(CSVExportMixin, CategoryDatasetsView):
    paginate_by = None
