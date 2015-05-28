from django.db import models
from common.models import TimestampedModel
from postgres.fields import JSONField  # Using schinckel/django-postgres until Django 1.9
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Crawl(TimestampedModel):
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Crawl"
        verbose_name_plural = "Crawls"

    def __str__(self):
        return self.id


class URLInspection(TimestampedModel):
    crawl = models.ForeignKey('Crawl', blank=True, null=True, on_delete=models.SET_NULL)
    url = models.URLField(max_length=500)
    response_meta = JSONField(default={})
    exists = models.NullBooleanField(help_text='URL resource exists')
    last_visited = models.DateTimeField(null=True, blank=True,
                                        help_text='Datetime when the URL was last visited')

    class Meta:
        verbose_name = "URL Inspection"
        verbose_name_plural = "URL Inspections"

    def __str__(self):
        return "Inspection of '{}'".format(self.url)


class RelatedObject(models.Model):
    inspection = models.OneToOneField('URLInspection', related_name='related')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "Related Object"
        verbose_name_plural = "Related Objects"

    def __str__(self):
        return 'URLInspection[{}] → {}'.format(self.inspection.id, self.object)

