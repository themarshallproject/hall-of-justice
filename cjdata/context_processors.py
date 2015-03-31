from cjdata.models import Category, STATE_NATL_CHOICES


def main_categories(request):
    return {'main_categories': Category.objects.filter(parent__isnull=True)}


def state_choices(request):
    return {'state_choices': STATE_NATL_CHOICES}
