from django.db import models
from django.contrib.postgres.fields import ArrayField
from localflavor.us.us_states import STATE_CHOICES
from django.core.urlresolvers import reverse
import uuid

STATE_NATL_CHOICES = (('US', 'National'),) + STATE_CHOICES
STATE_NATL_LOOKUP = dict(STATE_NATL_CHOICES)


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = 'created_at'
        ordering = ('-updated_at', '-created_at',)


class Category(TimestampedModel):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", related_name="children", null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['parent__name', 'name']

    @property
    def pathname(self):
        if self.parent:
            return "{parent_name}/{o.name}".format(o=self, parent_name=str(self.parent))
        else:
            return "{o.name}".format(o=self)

    def __str__(self):
        return self.pathname


class Dataset(TimestampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    states = ArrayField(models.CharField(choices=STATE_NATL_CHOICES, max_length=2), default=[])
    location = models.TextField(blank=True)
    sublocation = models.CharField(blank=True, max_length=150)
    categories = models.ManyToManyField("Category")
    title = models.TextField()
    description = models.TextField(blank=True)
    formats = ArrayField(models.CharField(max_length=40), blank=True, default=[],
                         help_text="Enter formats, separated by commas")
    url = models.URLField(blank=True, null=True, max_length=500)
    sectors = ArrayField(models.CharField(max_length=40), blank=True, default=[],
                         help_text="Sectors such as 'Private' or 'Government' or 'Non-Profit', separated by commas")
    group_name = models.CharField(help_text="Name of group administering dataset", max_length=150)
    associated_legislation = models.TextField(blank=True)
    internet_available = models.NullBooleanField()
    population_data = models.NullBooleanField()
    mappable = models.NullBooleanField()
    updated = models.NullBooleanField()
    frequency = models.CharField(blank=True, max_length=50)
    data_range = models.CharField(blank=True, max_length=100)
    associated_grant = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=50), blank=True, default=[],
                      help_text="Tags, separated by commas")
    access_type = models.CharField(blank=True, max_length=50)

    class Meta:
        verbose_name = "Dataset"
        verbose_name_plural = "Datasets"

    def states_expanded(self):
        return (STATE_NATL_LOOKUP[s] for s in self.states)

    def get_states_display(self):
        return ", ".join(self.states_expanded())

    def get_states_abbr_display(self):
        return ", ".join(self.states)

    def get_absolute_url(self):
        return reverse('dataset-detail', args=[str(self.uuid)])

    def __str__(self):
        return "{states} ({sectors}): {title}".format(states=self.get_states_display(),
                                                      title=self.title,
                                                      sectors=",".join(self.sectors))
