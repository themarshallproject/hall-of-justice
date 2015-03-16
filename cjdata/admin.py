from django.contrib import admin
from cjdata.models import (Category, Dataset)


class CategoryAdmin(admin.ModelAdmin):
    '''
        Admin View for Category
    '''
    list_display = ('pathname', 'name', 'parent', 'created_at', 'updated_at')
    search_fields = ['name', ]


class DatasetAdmin(admin.ModelAdmin):
    '''
        Admin View for Dataset
    '''
    list_display = ('title', 'states', 'tags', 'url', 'created_at', 'updated_at')
    list_filter = ('states',)
    search_fields = ['title', 'description', 'tags']
    filter_horizontal = ('categories',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Dataset, DatasetAdmin)
