from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from cjdata.models import Dataset, Category
from cjdata.search.query import sqs


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
        path_arg = self.kwargs.get('path', None)
        self.category = get_object_or_404(Category, path__iexact=path_arg.replace('-', ' '))
        return Dataset.objects.filter(categories__path=self.category.path)

    def get_context_data(self, **kwargs):
        context = super(CategoryDatasetsView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context
