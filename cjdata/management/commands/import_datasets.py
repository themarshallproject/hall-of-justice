from django.core.management.base import LabelCommand
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from csv import DictReader
import os
from cjdata.models import (Category, Dataset, STATE_NATL_LOOKUP)

validate_url = URLValidator()


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
                "format": "formats",
            }
            array_fields = ("tags", "formats", "sectors", "states",)
            for old_key, new_key in mappings.items():
                value = item.pop(old_key, None)
                if value:
                    if new_key in array_fields:
                        value = [v.strip() for v in value.split(",") if v.strip() != '']
                    item[new_key] = value

        def fix_states(item):
            if 'state' in item:
                value = item.pop('state', '')
                values_set = (v.strip() for v in value.split(","))
                values_set = ('US' if v.startswith('Nat') else v for v in values_set)
                values_set = (v for v in values_set if v in STATE_NATL_LOOKUP.keys())
                item['states'] = list(values_set)

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
                url = item['url'].strip()
                try:
                    validate_url(url)
                    item['url'] = url
                except ValidationError:
                    del item['url']

        # Actual script exection
        if os.path.exists(label):
            with open(label, 'r') as fp:
                reader = DictReader(fp)
                data_rows = [r for r in reader]
                for item in data_rows:
                    reformat_dict(item)
                    fix_states(item)
                    remap_keys(item)
                    booleanize(item)
                    fix_url(item)
                    self.stdout.write("Title: '{}'".format(item.get('title')))
                    if item.get('url'):
                        self.stdout.write("\tURL: '{}'".format(item.get('url')))
                    top_cat_name = item.pop('category', None)
                    sub_cat_name = item.pop('subcategory', None)
                    cat_obj = top_cat = None
                    if top_cat_name:
                        top_cat_name = top_cat_name.title().replace('/', ' & ')
                        try:
                            top_cat = Category.objects.get(name__iexact=top_cat_name, parent__isnull=True)
                            self.stdout.write("\tFound '{}' category".format(top_cat_name))
                            cat_obj = top_cat
                        except Category.MultipleObjectsReturned:
                            self.stderr.write("\tMultiple category matches for {}".format(top_cat_name))
                        except Category.DoesNotExist:
                            self.stderr.write("\tNo '{}' category".format(top_cat_name))
                        if sub_cat_name:
                            sub_cat_name = sub_cat_name.title().replace('/', ' & ')
                            cat_path = "{}/{}".format(top_cat_name, sub_cat_name)
                            try:
                                cat_obj = Category.objects.get(name__iexact=sub_cat_name, parent=top_cat)
                                self.stdout.write("\tFound '{}' subcategory".format(top_cat_name))
                            except Category.MultipleObjectsReturned:
                                self.stderr.write("\tMultiple subcategory matches for {}".format(cat_path))
                            except Category.DoesNotExist:
                                self.stderr.write("\tNo '{}' category.".format(cat_path))
                    # If we don't have a title and a group_name,we probably shouldn't create an entry.
                    if item.get('title', None) and item.get('group_name', None):
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
                                self.stderr.write("Failed to save dataset '{}':\n\t{}".format(item.get('title', ''), str(e)))
                                self.stderr.write("\n".join(["{}: {}".format(k,str(v)) for k,v in item.items()]))
                        if dataset:
                            self.stdout.write("\tCreated Dataset: {}\n".format(dataset))
                    else:
                        self.stderr.write("\tNot enough data to create a dataset! Need at least a title and group_name".format(item_str))
        else:
            self.stderr.write('File does not exist at path: {}'.format(label))
