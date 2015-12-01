# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import postgres.fields
import decimal
import django.db.models.deletion
import django.core.serializers.json


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crawl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Crawl',
                'verbose_name_plural': 'Crawls',
            },
        ),
        migrations.CreateModel(
            name='RelatedObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Related Object',
                'verbose_name_plural': 'Related Objects',
            },
        ),
        migrations.CreateModel(
            name='URLInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.URLField(max_length=500)),
                ('response_meta', postgres.fields.JSONField(default={}, decode_kwargs={'parse_float': decimal.Decimal}, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder})),
                ('exists', models.NullBooleanField(help_text='URL resource exists')),
                ('last_visited', models.DateTimeField(null=True, blank=True, help_text='Datetime when the URL was last visited')),
                ('crawl', models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='crawler.Crawl')),
            ],
            options={
                'verbose_name': 'URL Inspection',
                'verbose_name_plural': 'URL Inspections',
            },
        ),
        migrations.AddField(
            model_name='relatedobject',
            name='inspection',
            field=models.OneToOneField(related_name='related', to='crawler.URLInspection'),
        ),
    ]
