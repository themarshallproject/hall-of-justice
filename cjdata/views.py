from django.views.generic.detail import DetailView
from cjdata.models import Dataset


class DatasetDetailView(DetailView):
    model = Dataset
