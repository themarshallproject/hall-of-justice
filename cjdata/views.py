from django.views.generic.detail import DetailView
from cjdata.models import Dataset


class DatasetDetailView(DetailView):
    model = Dataset
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
