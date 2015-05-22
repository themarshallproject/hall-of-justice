from haystack.management.commands import update_index
from celery import shared_task


@shared_task
def update_search_index(age=24):
    update_index.Command().handle(using=['default'], age=age)
