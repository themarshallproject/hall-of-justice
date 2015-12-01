# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.utils.text import slugify


def categories_from_markdown(apps, schema_editor):
    Category = apps.get_model("cjdata", "Category")
    db_alias = schema_editor.connection.alias
    top_level_li = '- '
    sublevel_li = '    - '
    with open('cjdata/fixtures/categories.md', 'r') as fp:
        lines = fp.readlines()
        top_cat = None
        for l in lines:
            if l.startswith(top_level_li):
                cat_name = l.lstrip(top_level_li).strip()
                top_cat, created = Category.objects.using(db_alias).get_or_create(name=cat_name, parent__isnull=True)
                top_cat.slug = slugify(top_cat.name)
                top_cat.save()
            elif l.startswith(sublevel_li) and top_cat:
                cat_name = l.lstrip(sublevel_li).strip()
                sub_cat, created = Category.objects.using(db_alias).get_or_create(name=cat_name, parent=top_cat)
                sub_cat.slug = slugify(sub_cat.name)
                sub_cat.save()


def destroy_all_categories(apps, schema_editor):
    Category = apps.get_model("cjdata", "Category")
    db_alias = schema_editor.connection.alias
    Category.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cjdata', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(categories_from_markdown,
                             reverse_code=destroy_all_categories)
    ]
