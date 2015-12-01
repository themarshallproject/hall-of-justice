from django.conf.urls import patterns, url
from crawler.views import (CrawlDetailView, CrawlListView, URLInspectionDetailView)

urlpatterns = patterns(
    'crawler.views',
    url(r'crawls/$', CrawlListView.as_view(), name='crawl-list'),
    url(r'crawls/(?P<pk>[0-9]+)/$', CrawlDetailView.as_view(), name='crawl-detail'),
    url(r'url-inspections/(?P<pk>[0-9]+)/$', URLInspectionDetailView.as_view(), name='urlinspection-detail'),
)
