from django.contrib import admin
from cjdata.models import (Category, Dataset)


class CategoryAdmin(admin.ModelAdmin):
    '''
        Admin View for Category
    '''
    list_display = ('name', 'parent')


class DatasetAdmin(admin.ModelAdmin):
    '''
        Admin View for Dataset
    '''
    list_display = ('title', 'state', 'tags', 'url')
    list_filter = ('state',)
    search_fields = ['title', 'description', 'tags']
    filter_horizontal = ('categories',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Dataset, DatasetAdmin)
