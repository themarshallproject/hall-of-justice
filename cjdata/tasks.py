from haystack.management.commands import update_index
from celery import shared_task, group
from crawler.tasks import inspect_url
from crawler.models import Crawl
from cjdata.models import Dataset


@shared_task
def update_search_index(age=24):
    update_index.Command().handle(using=['default'], age=age)


@shared_task
def inspect_all_dataset_urls():
    tasks = []
    qs = Dataset.objects.all()
    crawl = Crawl.objects.create()
    for obj in qs:
        obj_info = {
            'app_label': 'cjdata',
            'model': 'dataset',
            'id': obj.id,
            'crawl_id': crawl.id
        }
        task = inspect_url.subtask((obj.url,),
                                   {'related_object': obj_info},
                                   countdown=2)
        tasks.append(task)
    g = group(tasks)
    return g()
