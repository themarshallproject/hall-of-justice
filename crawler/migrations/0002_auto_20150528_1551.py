# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crawl',
            options={'get_latest_by': 'created_at', 'verbose_name': 'Crawl', 'verbose_name_plural': 'Crawls'},
        ),
        migrations.AlterModelOptions(
            name='relatedobject',
            options={'get_latest_by': 'created_at', 'verbose_name': 'Related Object', 'verbose_name_plural': 'Related Objects'},
        ),
        migrations.AlterModelOptions(
            name='urlinspection',
            options={'get_latest_by': 'created_at', 'verbose_name': 'URL Inspection', 'verbose_name_plural': 'URL Inspections'},
        ),
        migrations.AddField(
            model_name='crawl',
            name='related_crawl',
            field=models.ForeignKey(blank=True, null=True, to='crawler.Crawl'),
        ),
    ]
