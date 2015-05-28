from django.core.management.base import BaseCommand, CommandError
from crawler.models import Crawl
import csv


class Command(BaseCommand):
    help = "Report 'bad' urls (HTTP status 400+) for a given crawl"

    def add_arguments(self, parser):
        parser.add_argument('crawl_id', nargs=1, type=int)

    def handle(self, *args, **options):
        crawl_id = options['crawl_id'][0]
        try:
            crawl = Crawl.objects.get(id=crawl_id)
        except Crawl.DoesNotExist:
            raise CommandError('Crawl "{}" does not exist'.format(crawl_id))

        qs = crawl.urlinspection_set.filter(exists=False).order_by('url')

        def inspection_dict(i):
            return {
                'url': i.url,
                'status_code': i.response_meta.get('status_code', None),
                'server': i.response_meta['headers'].get('server', None),
                'content_type': i.response_meta['headers'].get('content-type', None),
                'is_redirect': i.response_meta.get('is_redirect', None),
                'seconds_elapsed': i.response_meta.get('seconds_elapsed', None),
            }

        fieldnames = ('url', 'status_code', 'server', 'content_type', 'is_redirect', 'seconds_elapsed')
        output = (inspection_dict(x) for x in qs)

        writer = csv.DictWriter(self.stdout, fieldnames, quoting=csv.QUOTE_ALL, extrasaction='ignore')
        writer.writeheader()

        for item in output:
            writer.writerow(item)
