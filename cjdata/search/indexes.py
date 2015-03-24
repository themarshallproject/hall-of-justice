from haystack import indexes
from cjdata.models import Dataset
import datetime


class DatasetIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', boost=1.25)
    description = indexes.CharField(model_attr='description', boost=1.125)
    group_name = indexes.CharField(model_attr='group_name', faceted=True)
    states = indexes.FacetMultiValueField(model_attr='states')
    sectors = indexes.FacetMultiValueField(model_attr='sectors')
    tags = indexes.MultiValueField(model_attr='tags', boost=0.8)
    formats = indexes.MultiValueField(model_attr='formats', boost=0.6)

    class Meta:
        model = Dataset
        excludes = ['uuid', 'created_at', 'updated_at', 'formats']

    def prepare_states(self, obj):
        states_list = list(obj.states_expanded())
        return states_list

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(updated_at__lte=datetime.datetime.now())
