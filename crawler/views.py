from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from crawler.models import (Crawl, URLInspection)


class CrawlDetailView(SingleObjectMixin, ListView):
    model = Crawl
    paginate_by = 50
    template_name = 'crawler/crawl_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Crawl.objects.all())
        return super(CrawlDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CrawlDetailView, self).get_context_data(**kwargs)
        context['crawl'] = self.object
        return context

    def get_queryset(self):
        # Paginate inspection objects
        return self.object.urlinspection_set.order_by('url')


class CrawlListView(ListView):
    model = Crawl
    paginate_by = 50
    ordering = ('-created_at',)


class URLInspectionDetailView(DetailView):
    model = URLInspection

