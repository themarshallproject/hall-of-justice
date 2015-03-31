from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin
from django.shortcuts import get_object_or_404
from cjdata.models import Dataset, Category
from cjdata.search.query import sqs


class CategoryContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
            context = super(CategoryContextMixin, self).get_context_data(**kwargs)
            context['categories'] = Category.objects.filter(parent__isnull=True)
            return context


class IndexView(TemplateView, CategoryContextMixin):
    template_name = "cjdata/index.html"


class DatasetDetailView(DetailView, CategoryContextMixin):
    model = Dataset
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super(DatasetDetailView, self).get_context_data(**kwargs)
        context['more_like_this'] = sqs.more_like_this(self.object)[:100]
        return context


class CategoryDatasetsView(ListView, CategoryContextMixin):
    model = Dataset
    paginate_by = 50

    def get_queryset(self):
        cat_slug = self.kwargs.get('category', None)
        subcat_slug = self.kwargs.get('subcategory', None)
        self.category = get_object_or_404(Category, slug=cat_slug, parent__isnull=True)
        if subcat_slug:
            self.category = get_object_or_404(Category, slug=subcat_slug, parent=self.category)
        return self.category.dataset_set.all()

    def get_context_data(self, **kwargs):
        context = super(CategoryDatasetsView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context
