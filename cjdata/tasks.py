from haystack.management.commands import (update_index, rebuild_index)
from celery import shared_task, group
from crawler.tasks import inspect_url
from crawler.models import Crawl
from cjdata.models import Dataset


@shared_task
def update_search_index(age=24):
    return update_index.Command().handle(using=['default'], age=age)


@shared_task
def rebuild_search_index(age=None):
    return rebuild_index.Command().handle(using=['default'], age=None, interactive=False)


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


@shared_task
def inspect_previously_bad_urls(previous_crawl_id):
    tasks = []
    try:
        previous_crawl = Crawl.objects.get(id=previous_crawl_id)
    except Crawl.DoesNotExist:
        previous_crawl = None
    if previous_crawl:
        # Get URLInspections from previous_crawl that has exists=False
        qs = previous_crawl.urlinspection_set.filter(exists=False)
        note_text = "Closer inspection of 'bad' urls from previous crawl with id {}".format(previous_crawl_id)
        crawl = Crawl.objects.create(notes=note_text, related_crawl_id=previous_crawl_id)
        for obj in qs:
            obj_info = {
                'app_label': 'cjdata',
                'model': 'dataset',
                'id': obj.id,
                'crawl_id': crawl.id
            }
            task = inspect_url.subtask((obj.url,),
                                       {
                                        'method': 'GET',
                                        'related_object': obj_info,
                                        'stream': True
                                        },
                                       countdown=2)
            tasks.append(task)
        g = group(tasks)
        return g()
    else:
        return None
