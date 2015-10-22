from django.db import models
from django.contrib.postgres.fields import ArrayField
from localflavor.us.us_states import STATE_CHOICES
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from common.models import TimestampedModel
import uuid

STATE_NATL_CHOICES = (('US', 'National'),) + STATE_CHOICES
STATE_NATL_LOOKUP = dict(STATE_NATL_CHOICES)

class Category(TimestampedModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=70, editable=False)
    parent = models.ForeignKey("self", related_name="children", null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['parent__name', 'name']
        unique_together = ("name", "parent")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    @property
    def path(self):
        return self._calculate_pathname(False)

    @property
    def slugged_path(self):
        return self._calculate_pathname(True)

    def _calculate_pathname(self, slugged):
        name = self.slug if slugged else self.name

        if self.parent:
            parent_name = str(self.parent.slug) if slugged else str(self.parent.name)
            return "{parent_name}/{name}".format(name=name, parent_name=parent_name)
        else:
            return "{name}".format(name=name)

    def get_absolute_url(self):
        kwargs = {'category': self.parent.slug if self.parent else self.slug}
        if self.parent:
            kwargs['subcategory'] = self.slug
        return reverse('datasets-by-category', kwargs=kwargs)

    def __str__(self):
        return self.path


class Dataset(TimestampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    # General
    title = models.TextField()
    url = models.URLField(blank=True, null=True, max_length=500)
    description = models.TextField(blank=True)
    group_name = models.CharField(db_index=True, max_length=150,
                                  help_text="Name of group administering dataset.")
    categories = models.ManyToManyField("Category")
    tags = ArrayField(models.CharField(max_length=50), blank=True, default=[],
                      help_text="Tags, separated by commas.")
    # Location
    states = ArrayField(models.CharField(choices=STATE_NATL_CHOICES, max_length=2), default=[],
                        help_text="List of state abbreviations: NC, CA, PA, etc. Use 'US' for a national dataset")
    division_names = ArrayField(models.CharField(max_length=150), default=[],
                                help_text='Describes one or more geographic divisions such as a city or county.')
    # Resource Information
    resource_location = models.TextField(blank=True,
                                         help_text='Describes where in a resource to find the dataset.')
    updated = models.NullBooleanField(help_text="Does this resource get updated?")
    frequency = models.CharField(blank=True, max_length=50,
                                 help_text="How often this resource is updated.")
    sectors = ArrayField(models.CharField(max_length=40), blank=True, default=[],
                         help_text="Sectors responsible for the data resource, such as \
                                    'Private' or 'Government' or 'Non-Profit', separated by commas.")
    # Data Properties
    mappable = models.NullBooleanField(help_text="Can the information be put on a map, i.e. a crime map?")
    population_data = models.NullBooleanField(help_text="Does this dataset include population data?")
    formats = ArrayField(models.CharField(max_length=40), blank=True, default=[],
                         help_text="Enter formats, separated by commas")
    data_range = models.CharField(blank=True, max_length=100,
                                  help_text="Human-readable description of the time period covered in the data.")
    # Availability
    internet_available = models.NullBooleanField(help_text="Is this dataset available online?")
    access_type = models.CharField(db_index=True, blank=True, max_length=50,
                                   help_text="Description of how data can be accessed, and if it is machine readable.")
    # Associated Information
    associated_legislation = models.TextField(blank=True)
    associated_grant = models.TextField(blank=True,
                                        help_text="Name of associated grant that funds the dataset, if available.")

    class Meta:
        get_latest_by = 'created_at'
        verbose_name = "Dataset"
        verbose_name_plural = "Datasets"
        ordering = ['states', '-updated_at', 'url']

    def states_expanded(self):
        return (STATE_NATL_LOOKUP[s] for s in self.states)

    def get_states_display(self):
        return ", ".join(self.states_expanded())

    def get_states_abbr_display(self):
        return ", ".join(self.states)

    def get_division_names_display(self):
        return ", ".join(self.division_names)

    def get_absolute_url(self):
        return reverse('dataset-detail', args=[str(self.uuid)])

    def __str__(self):
        return "{states} ({sectors}): {title}".format(states=self.get_states_display(),
                                                      title=self.title,
                                                      sectors=",".join(self.sectors))
