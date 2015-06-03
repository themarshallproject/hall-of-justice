from django.views.generic import DetailView, ListView, TemplateView
from django.shortcuts import get_object_or_404
from cjdata.models import Dataset, Category, STATE_NATL_LOOKUP
from search.query import sqs


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


class CategoryDatasetsView(ListView):
    model = Dataset
    paginate_by = 50

    def get_queryset(self):
        cat_slug = self.kwargs.get('category', None)
        subcat_slug = self.kwargs.get('subcategory', None)
        if cat_slug != 'none':
            self.category = get_object_or_404(Category, slug=cat_slug, parent__isnull=True)
            if subcat_slug:
                self.category = get_object_or_404(Category, slug=subcat_slug, parent=self.category)
            return self.category.dataset_set.all()
        else:
            return Dataset.objects.filter(categories__isnull=True)

    def get_context_data(self, **kwargs):
        context = super(CategoryDatasetsView, self).get_context_data(**kwargs)
        context['category'] = getattr(self, 'category', None)
        return context


class StateDatasetsView(ListView):
    model = Dataset
    paginate_by = 50

    def get_queryset(self):
        self.state_abbr = self.kwargs.get('location', '').upper()
        return Dataset.objects.filter(states__contains=[self.state_abbr])

    def get_context_data(self, **kwargs):
        context = super(StateDatasetsView, self).get_context_data(**kwargs)
        context['location_abbr'] = self.state_abbr
        context['location'] = STATE_NATL_LOOKUP.get(self.state_abbr, None)
        return context
