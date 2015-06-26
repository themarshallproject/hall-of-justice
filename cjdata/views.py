from django.views.generic import View, DetailView, ListView, TemplateView
from django.shortcuts import get_object_or_404
from cjdata.models import Dataset, Category, STATE_NATL_LOOKUP
from search.query import sqs
from django.http import StreamingHttpResponse
import csv
import itertools


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


class Echo(object):

    """An object that implements just the write method of the file-like interface."""

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


class DataExportView(View):

    def get(self, request, *args, **kwargs):
        def generate_rows(queryset, fieldnames):
            for object in qs:
                yield list(getattr(object, f, None) for f in fieldnames)

        output_fieldnames = [f.name for f in Dataset._meta.get_fields() if f.name != 'id']
        qs = Dataset.objects.all()

        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        rows = generate_rows(qs, output_fieldnames)
        rows_with_header = itertools.chain((writer.writerow(header) for header in (output_fieldnames,)),
                                           (writer.writerow(row) for row in rows))

        response = StreamingHttpResponse(rows_with_header, content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="criminal-justice-{}-rows.csv"'.format(qs.count())
        return response
