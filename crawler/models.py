from django.db import models
from common.models import TimestampedModel
from postgres.fields import JSONField  # Using schinckel/django-postgres until Django 1.9


class URLInspection(TimestampedModel):
    url = models.URLField(max_length=500)
    response_meta = JSONField(default={})
    valid = models.NullBooleanField(help_text='URL is valid')
    exists = models.NullBooleanField(help_text='URL resource exists')

    class Meta:
        verbose_name = "URL Inspection"
        verbose_name_plural = "URL Inspections"

    def __str__(self):
        return "Inspection of '{}'".format(self.url)
