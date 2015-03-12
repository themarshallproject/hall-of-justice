from django.db import models
from django.contrib.postgres.fields import ArrayField


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", related_name="children")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categoryies"

    def __str__(self):
        if self.parent:
            return "{parent_name}/{o.name}".format(o=self, parent_name=str(self.parent))
        else:
            return "{o.name}".format(o=self)


class Dataset(models.Model):
    state = models.CharField(max_length=32)
    sublocation = models.CharField(max_length=128)
    categories = models.ManyToManyField("Category")
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    formats = ArrayField(models.CharField(max_length=32))
    url = models.URLField(blank=True, null=True)
    sectors = ArrayField(models.CharField(max_length=32),
                         help_text="Sectors such as 'Private' or 'Government' or 'Non-Profit'")
    group_name = models.CharField(help_text="Name of group administering dataset", max_length=150)
    location = models.CharField(blank=True, null=True, max_length=64)
    associated_legislation = models.CharField(blank=True, null=True, max_length=150)
    internet_available = models.NullBooleanField()
    population_data = models.NullBooleanField()
    mappable = models.NullBooleanField()
    updated = models.NullBooleanField()
    frequency = models.CharField(blank=True, null=True, max_length=50)
    data_range = models.CharField(blank=True, null=True, max_length=100)
    associated_grant = models.CharField(blank=True, null=True, max_length=100)
    tags = ArrayField(models.CharField(max_length=50))
    access_type = models.CharField(blank=True, null=True, max_length=50)

    class Meta:
        verbose_name = "Dataset"
        verbose_name_plural = "Datasets"

    def __str__(self):
        return "{o.state} ({o.private_or_government}): {o.title}".format(o=self)
