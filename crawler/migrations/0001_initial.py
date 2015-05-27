# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import postgres.fields
import decimal
import django.core.serializers.json


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedObject',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'Related Objects',
                'verbose_name': 'Related Object',
            },
        ),
        migrations.CreateModel(
            name='URLInspection',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.URLField(max_length=500)),
                ('response_meta', postgres.fields.JSONField(decode_kwargs={'parse_float': decimal.Decimal}, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, default={})),
                ('exists', models.NullBooleanField(help_text='URL resource exists')),
                ('last_visited', models.DateTimeField(help_text='Datetime when the URL was last visited', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'URL Inspections',
                'verbose_name': 'URL Inspection',
            },
        ),
        migrations.AddField(
            model_name='relatedobject',
            name='inspection',
            field=models.OneToOneField(to='crawler.URLInspection'),
        ),
    ]
