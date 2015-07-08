from django.core.management.base import BaseCommand
from django.utils.text import slugify
from cjdata.models import Category
import argparse
from common.utils import parse_markdown_list


class Command(BaseCommand):
    help = 'Given a markdown list of category names, \
    will create entries for any that are missing from the Category table'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('filepath', nargs='?', type=argparse.FileType('r'))

        # Named (optional) arguments
        parser.add_argument('-n', '--dry-run',
                            action='store_true',
                            dest='dryrun',
                            default=False,
                            help='Run through file and output errors, but don\'t save datasets')

    def handle(self, *args, **options):
        fp = options.get('filepath', None)
        save_objects = not options.get('dryrun', False)
        verbosity = options.get('verbosity', None)

        if fp:
            top_cat = None
            list_items = parse_markdown_list(fp.read())
            for indent, item in list_items:
                cat_name = item.strip()
                if indent < 2:
                    if verbosity > 1:
                        self.stdout.write("Found top-level category name '{}'".format(cat_name))
                    try:
                        top_cat = Category.objects.get(name__iexact=cat_name, parent__isnull=True)
                        if verbosity > 1:
                            self.stdout.write("Existing category: '{}'".format(top_cat.path))
                    except Category.DoesNotExist:
                        top_cat = Category(name=cat_name)
                        self.stdout.write("New category: '{}'".format(top_cat))
                    top_cat.slug = slugify(top_cat.name)
                    if save_objects:
                        if verbosity > 1:
                            self.stdout.write("Saving top-level category: '{}'".format(top_cat.name))
                        top_cat.save()
                elif indent >= 2 and top_cat:
                    if verbosity > 1:
                        self.stdout.write("Found subcategory '{} -> {}'".format(top_cat.name, cat_name))
                    if save_objects:
                        try:
                            sub_cat = Category.objects.get(name__iexact=cat_name, parent=top_cat)
                            if verbosity > 1:
                                self.stdout.write("Existing subcategory: '{}'".format(sub_cat.path))
                        except Category.DoesNotExist:
                            sub_cat = Category(name=cat_name, parent=top_cat)
                            self.stdout.write("New category: '{}'".format(sub_cat))
                        sub_cat.slug = slugify(sub_cat.name)

                        sub_cat.save()
                        if verbosity > 1:
                            self.stdout.write("Saving subcategory: '{}'".format(sub_cat.name))
                else:
                    self.stderr.write("Line that isn't list-like")

        else:
            self.stderr.write("File path not provided. Please provide a path to a markdown file to process")
