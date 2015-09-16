# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cjdata', '0003_add_indexes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='group_name',
            field=models.CharField(db_index=True, max_length=150, help_text='Name of group administering dataset.'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='sectors',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=40), default=[], help_text="Sectors responsible for the data resource, such as                                     'Private' or 'Government' or 'Non-Profit', separated by commas.", blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='states',
            field=django.contrib.postgres.fields.ArrayField(default=[], help_text="List of state abbreviations: NC, CA, PA, etc. Use 'US' for a national dataset", base_field=models.CharField(max_length=2, choices=[('US', 'National'), ('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]), size=None),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), default=[], help_text='Tags, separated by commas.', blank=True, size=None),
        ),
    ]
