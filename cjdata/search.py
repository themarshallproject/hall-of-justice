from haystack.query import SearchQuerySet

sqs = SearchQuerySet().facet('states').facet('group_name').facet('tags').facet('sectors')
