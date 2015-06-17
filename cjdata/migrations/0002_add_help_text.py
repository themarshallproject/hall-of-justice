# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cjdata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='access_type',
            field=models.CharField(max_length=50, blank=True, help_text='Description of how data can be accessed, and if it is machine readable.'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='associated_grant',
            field=models.TextField(help_text='Name of associated grant that funds the dataset, if available.', blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='data_range',
            field=models.CharField(max_length=100, blank=True, help_text='Human-readable description of the time period covered in the data.'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='division_names',
            field=django.contrib.postgres.fields.ArrayField(size=None, base_field=models.CharField(max_length=150), default=[], help_text='Describes one or more geographic divisions such as a city or county.'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='frequency',
            field=models.CharField(max_length=50, blank=True, help_text='How often this resource is updated.'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='internet_available',
            field=models.NullBooleanField(help_text='Is this dataset available online?'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='mappable',
            field=models.NullBooleanField(help_text='Can the information be put on a map, i.e. a crime map?'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='population_data',
            field=models.NullBooleanField(help_text='Does this dataset include population data?'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='resource_location',
            field=models.TextField(help_text='Describes where in a resource to find the dataset.', blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='sectors',
            field=django.contrib.postgres.fields.ArrayField(size=None, help_text="Sectors such as 'Private' or 'Government' or 'Non-Profit', separated by commas.", default=[], blank=True, base_field=models.CharField(max_length=40)),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='updated',
            field=models.NullBooleanField(help_text='Does this resource get updated?'),
        ),
    ]
