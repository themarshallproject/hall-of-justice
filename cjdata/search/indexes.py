from haystack import indexes
from elasticstack.fields import EdgeNgramField
from cjdata.models import Dataset, Category
import datetime


class DatasetIndex(indexes.ModelSearchIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='title', boost=1.25)
    description = indexes.CharField(model_attr='description', boost=1.125)
    group_name = indexes.CharField(model_attr='group_name', faceted=True)
    states = indexes.FacetMultiValueField(model_attr='states')
    sectors = indexes.FacetMultiValueField(model_attr='sectors')
    formats = indexes.MultiValueField(model_attr='formats', boost=0.6)

    class Meta:
        model = Dataset
        excludes = ['uuid', 'created_at', 'updated_at', 'formats', 'tags']

    def prepare_states(self, object):
        states_list = list(object.states_expanded())
        return states_list

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(updated_at__lte=datetime.datetime.now())


class CategoryIndex(indexes.ModelSearchIndex, indexes.Indexable):
    path = EdgeNgramField(model_attr='path', analyzer='edgengram_analyzer')

    class Meta:
        model = Category
        excludes = ['parent']

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(updated_at__lte=datetime.datetime.now())
