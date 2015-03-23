from haystack import indexes
from elasticstack.fields import CharField
from cjdata.models import Dataset
import datetime


class DatasetIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    states = indexes.FacetMultiValueField()
    sectors = indexes.FacetMultiValueField(model_attr='sectors')
    tags = indexes.FacetMultiValueField(model_attr='tags')
    group_name = indexes.CharField(model_attr='group_name', faceted=True)

    class Meta:
        model = Dataset
        fields = ['title', 'description', 'group_name']

    def prepare_states(self, obj):
        states_list = list(obj.states_expanded())
        return states_list

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(updated_at__lte=datetime.datetime.now())
