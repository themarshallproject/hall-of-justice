from haystack import indexes
from elasticstack.fields import EdgeNgramField, MultiValueField
from cjdata.models import Dataset, Category
import datetime


class DatasetIndex(indexes.ModelSearchIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='title', boost=1.25)
    description = indexes.CharField(model_attr='description', boost=1.125)
    group_name = indexes.CharField(model_attr='group_name', faceted=True)
    states = indexes.FacetMultiValueField(model_attr='states')
    division_names = indexes.FacetMultiValueField(model_attr='division_names')
    sectors = indexes.FacetMultiValueField(model_attr='sectors')
    formats = indexes.MultiValueField(model_attr='formats', boost=0.6)
    tags = indexes.MultiValueField(model_attr='tags', boost=0.6)

    class Meta:
        model = Dataset
        excludes = ['uuid', 'created_at', 'updated_at', 'formats', 'tags']

    def prepare_states(self, object):
        states_list = list(object.states_expanded())
        return states_list

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(updated_at__lte=datetime.datetime.now())

    def get_updated_field(self):
        return 'updated_at'


class CategoryIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = EdgeNgramField(document=True, analyzer='edgengram_analyzer')

    class Meta:
        model = Category
        fields = ['name']

    def prepare_text(self, object):
        return object.path

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(updated_at__lte=datetime.datetime.now())

    def get_updated_field(self):
        return 'updated_at'


class TagIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = MultiValueField(document=True, analyzer='edgengram_analyzer')

    class Meta:
        model = Dataset
        fields = ['title', 'group_name']

    def prepare_text(self, object):
        return object.tags

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(updated_at__lte=datetime.datetime.now())

    def get_updated_field(self):
        return 'updated_at'
