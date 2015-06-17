# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cjdata', '0002_add_help_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='group_name',
            field=models.CharField(help_text='Name of group administering dataset', max_length=150, db_index=True),
        ),
        migrations.RunSQL('CREATE INDEX cjdata_dataset_tags ON cjdata_dataset USING GIN(tags);',
                          reverse_sql='DROP INDEX cjdata_dataset_tags;'),

    ]
