from django.db import models
from django.contrib.postgres.fields import ArrayField


class Category(models.Model):
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


class Dataset(models.Model):
    state = models.CharField(max_length=40)
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
    location = models.TextField(blank=True)
    associated_legislation = models.TextField(blank=True)
    internet_available = models.NullBooleanField()
    population_data = models.NullBooleanField()
    mappable = models.NullBooleanField()
    updated = models.NullBooleanField()
    frequency = models.CharField(blank=True, max_length=50)
    data_range = models.CharField(blank=True, max_length=50)
    associated_grant = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=50), blank=True, default=[],
                      help_text="Tags, separated by commas")
    access_type = models.CharField(blank=True, max_length=50)

    class Meta:
        verbose_name = "Dataset"
        verbose_name_plural = "Datasets"

    def __str__(self):
        return "{o.state} ({sectors}): {o.title}".format(o=self, sectors=",".join(self.sectors))
