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
    list_display = ('title', 'group_name', 'get_states_display', 'tags', 'url', 'created_at', 'updated_at')
    search_fields = ['title', 'description', 'tags', 'group_name']
    filter_horizontal = ('categories',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Dataset, DatasetAdmin)
