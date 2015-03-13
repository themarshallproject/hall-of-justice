from haystack import indexes
from cjdata.models import Dataset


class DatasetIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Dataset
        fields = ['title', 'description', 'state']
