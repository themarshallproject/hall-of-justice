from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AdminTextInputWidget
from cjdata.models import (Category, Dataset, STATE_NATL_CHOICES)


class StateListFilter(admin.SimpleListFilter):
    title = 'State'
    parameter_name = 'state'

    def lookups(self, request, model_admin):
        return STATE_NATL_CHOICES

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(states__contains=[self.value()])
        else:
            return queryset


class CategoryAdmin(admin.ModelAdmin):

    '''Admin View for Category'''
    list_display = ('path', 'name', 'parent', 'created_at', 'updated_at')
    search_fields = ['name', ]


class DatasetAdminForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = "__all__"
        widgets = {
            'tags': AdminTextInputWidget(attrs={'class': 'vTextField'}),
            'states': AdminTextInputWidget(attrs={'class': 'vTextField'}),
            'division_names': AdminTextInputWidget(attrs={'class': 'vTextField'}),
        }


class DatasetAdmin(admin.ModelAdmin):

    '''Admin View for Dataset'''
    form = DatasetAdminForm
    list_display = ('__str__', 'title', 'group_name', 'tags', 'url', 'created_at', 'updated_at')
    search_fields = ['title', 'description', 'tags', 'group_name']
    filter_horizontal = ('categories',)
    list_filter = (StateListFilter, 'group_name')
    list_editable = ('title', 'url', 'tags')
    readonly_fields = ('uuid',)
    fieldsets = (
        (None, {
            'fields': ('uuid',)
        }),
        ('General', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('url', 'title', 'group_name', 'description', 'categories', 'tags')
        }),
        ('Location', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('states', 'division_names')
        }),
        ('Resource Information', {
            'classes': ('grp-collapse grp-open',),
            'description': 'Whether the resource is updated, how frequently, etc.',
            'fields': ('updated', 'frequency', 'sectors', 'resource_location')
        }),
        ('Data Properties', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('mappable', 'population_data', 'data_range', 'formats')
        }),
        ('Availability', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('internet_available', 'access_type')
        }),
        ('Associated Items', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('associated_legislation', 'associated_grant')
        }),
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Dataset, DatasetAdmin)
