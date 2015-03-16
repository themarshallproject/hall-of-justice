from django.conf.urls import patterns, url

from cjdata.views import DatasetDetailView

urlpatterns = patterns('',
    url(r'^(?P<pk>[\d]+)/$', DatasetDetailView.as_view(), name='dataset-detail'),
)
