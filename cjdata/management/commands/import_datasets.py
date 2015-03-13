from django.core.management.base import LabelCommand
from django.db import transaction
from django.core.exceptions import ValidationError
import time

from csv import DictReader
import os
from cjdata.models import (Category, Dataset)


class Command(LabelCommand):
    args = '<filepath>'
    help = 'Imports datasets from a particularly formatted CSV'

    def handle_label(self, label, **options):
        # Define some helper functions for fiing field names
        def remap_keys(item):
            '''Some fields need manual remapping to Dataset field names'''
            mappings = {
                standardize_key("Private/Government"): "sectors",
                standardize_key("Is this data updated? (Y/N)"): "updated",
                # "category": "categories",
                "internet_availability": "internet_available",
                "tag": "tags",
                "format": "formats"
            }
            array_fields = ("tags", "formats", "sectors")
            for old_key, new_key in mappings.items():
                value = item.pop(old_key, None)
                if value:
                    if new_key in array_fields:
                        value = value.split(",")
                    item[new_key] = value

        def standardize_key(k):
            '''Many fields can be fixed by lowercasing and replacing certain characters'''
            return str(k).lower().strip().replace('? (y/n)', '').replace(' ', '_').replace('/', '_')

        def reformat_dict(item):
            '''Iterate overkeys and run standardize_key'''
            original_keys = list(item.keys())
            for original_key in original_keys:
                new_key = standardize_key(original_key)
                value = item.pop(original_key, None)
                if value:
                    item[new_key] = value

        def booleanize(item):
            boolean_fields = ("mappable", "updated", "population_data", "internet_available")
            for field in boolean_fields:
                value = item.get(field, None)
                if value:
                    item[field] = True if value.lower().startswith('y') else False
                else:
                    item[field] = None

        def fix_url(item):
            if 'url' in item:
                startswith_http = item['url'].lower().startswith('http')
                startswith_ftp = item['url'].lower().startswith('ftp')
                if not (startswith_http or startswith_ftp):
                    item['url'] = None

        # Actual script exection
        if os.path.exists(label):
            with open(label, 'r') as fp:
                reader = DictReader(fp)
                data_rows = [r for r in reader]
                for item in data_rows:
                    reformat_dict(item)
                    remap_keys(item)
                    booleanize(item)
                    fix_url(item)
                    top_cat_name = item.pop('category', None)
                    sub_cat_name = item.pop('subcategory', None)
                    cat_obj = top_cat = None
                    # import ipdb; ipdb.set_trace()
                    if top_cat_name:
                        try:
                            top_cat = Category.objects.get(name=top_cat_name, parent__isnull=True)
                            cat_obj = top_cat
                        except Category.MultipleObjectsReturned:
                            print("Multiple matches for {}".format(top_cat_name))
                        except Category.DoesNotExist:
                            print("No '{}' category".format(top_cat_name))
                        if sub_cat_name:
                            cat_path = "{}/{}".format(top_cat_name, sub_cat_name)
                            try:
                                cat_obj = Category.objects.get(name=sub_cat_name, parent=top_cat)
                            except Category.MultipleObjectsReturned:
                                print("Multiple matches for {}".format(cat_path))
                            except Category.DoesNotExist:
                                print("No '{}' category".format(cat_path))
                    if item.get('title', None) and item.get('state', None) and item.get('group_name'):
                        dataset = None
                        with transaction.atomic():
                            dataset = Dataset.objects.create(**item)
                            if cat_obj:
                                cat_obj.dataset_set.add(dataset)
                                cat_obj.save()
                            try:
                                dataset.full_clean()
                                dataset.save()
                            except ValidationError as e:
                                self.stderr.write(str(e))
                        if dataset:
                            self.stdout.write("Created Dataset: {}\n".format(dataset))
        else:
            self.stderr.write('File does not exist at path: {}'.format(label))
