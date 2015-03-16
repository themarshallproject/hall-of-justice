from haystack import indexes
from cjdata.models import Dataset
import datetime


class DatasetIndex(indexes.ModelSearchIndex, indexes.Indexable):
    states = indexes.MultiValueField(faceted=True)

    class Meta:
        model = Dataset
        fields = ['title', 'description']

    def prepare_states(self, obj):
            states_list = list(obj.states_expanded())
            states_list.extend(obj.states)
            return states_list

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(updated_at__lte=datetime.datetime.now())
