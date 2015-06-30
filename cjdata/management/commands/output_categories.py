from django.core.management.base import BaseCommand
from cjdata.models import Category


class Command(BaseCommand):
    help = 'Prints a list of categories and subcategories to stdout'

    def handle(self, *args, **kargs):
        for topcat in Category.objects.filter(parent__isnull=True):
            self.stdout.write("- {}".format(topcat.name))

            for subcat in Category.objects.filter(parent=topcat):
                self.stdout.write("    - {}".format(subcat.name))
