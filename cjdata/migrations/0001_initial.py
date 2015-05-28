# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=70, editable=False)),
                ('path', models.CharField(max_length=200, editable=False)),
                ('parent', models.ForeignKey(null=True, to='cjdata.Category', blank=True, related_name='children')),
            ],
            options={
                'ordering': ['path', 'parent__name', 'name'],
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(editable=False, default=uuid.uuid4)),
                ('states', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=2, choices=[('US', 'National'), ('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]), size=None, default=[])),
                ('division_names', django.contrib.postgres.fields.ArrayField(help_text='Describes one or more geographic divisions such as a city or county', size=None, base_field=models.CharField(max_length=150), default=[])),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('formats', django.contrib.postgres.fields.ArrayField(size=None, help_text='Enter formats, separated by commas', blank=True, base_field=models.CharField(max_length=40), default=[])),
                ('url', models.URLField(blank=True, max_length=500, null=True)),
                ('resource_location', models.TextField(help_text='Describes where in a resource to find the dataset', blank=True)),
                ('sectors', django.contrib.postgres.fields.ArrayField(size=None, help_text="Sectors such as 'Private' or 'Government' or 'Non-Profit', separated by commas", blank=True, base_field=models.CharField(max_length=40), default=[])),
                ('group_name', models.CharField(max_length=150, help_text='Name of group administering dataset')),
                ('associated_legislation', models.TextField(blank=True)),
                ('internet_available', models.NullBooleanField()),
                ('population_data', models.NullBooleanField()),
                ('mappable', models.NullBooleanField()),
                ('updated', models.NullBooleanField()),
                ('frequency', models.CharField(max_length=50, blank=True)),
                ('data_range', models.CharField(max_length=100, blank=True)),
                ('associated_grant', models.TextField(blank=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(size=None, help_text='Tags, separated by commas', blank=True, base_field=models.CharField(max_length=50), default=[])),
                ('access_type', models.CharField(max_length=50, blank=True)),
                ('categories', models.ManyToManyField(to='cjdata.Category')),
            ],
            options={
                'ordering': ['-updated_at', 'url'],
                'verbose_name_plural': 'Datasets',
                'verbose_name': 'Dataset',
            },
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('name', 'parent')]),
        ),
    ]
