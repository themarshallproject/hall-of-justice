# hall-of-justice

Working with criminal justice data.

## Setup

*A work in progress. The set up will almost certainly change in the near future.*

You can take a properly formatted (fits the data schema) xlsx file and collapse it to a single csv using `scripts/collapse_xls_to_csv.py`. This csv can be imported into a Django database (already created using `python manage.py migrate`) using the *import_datasets* management command, i.e.: `python manage.py import_datasets /path/to/data.csv -v 3 2> import_errors.log`.

You can look for errors around datasets that failed to import (`grep '^Failed to save dataset' import_errors.log | sort`) or categories that don't exist (`grep category$ import_errors.log | uniq | sort`). There are also  rows from the csv where there wasn't enough data to create a dataset (*Not enough data to create a dataset!*), but those are likely mostly empty rows from the input csv.

Once you've imported data into the database, you should create (or recreate) the elasticsearch search index using `python manage.py rebuild_index`.

## Development

There is a Vagrantfile for setting up multiple Virtualbox virtual machines and provisioning them using [Ansible](http://docs.ansible.com). You should be able to run `vagrant up` to create the machines. You'll need to run the setup steps above to populate the data.

Further information is available in NOTES.md.

## Feature Notes

### Search

The Elasticsearch features are implemented using [haystack](http://django-haystack.readthedocs.org/en/v2.4.0/) and [elasticstack](https://github.com/bennylope/elasticstack), plus a number of custom forms, views, etc. that live in the *search* app. The core feature supported with this mish-mash is a custom analyzer that supports criminal justice synonyms, as seen in `search/settings.py`. The tl;dr on the custom backend is that default haystack search uses the search query language (*query_string* query) that is incompatible with the synonym filter. Hence `search.backends.PliableSearchBackend` which performs an Elasticsearch *match* query by default, but *query_string* can be enabled as an alternative (but disables the synonym filter).

### Crawler

There is a *crawler* app that provides [Celery](http://docs.celeryproject.org/en/latest/index.html) tasks for crawling/inspecting URLs. The `cjdata.tasks.inspect_all_dataset_urls` task will spawn subtasks to inspect all Dataset URLs in the database. That function calls `crawler.tasks.inspect_url` for each Dataset's URL and records the relation back to the original Dataset. `crawler.tasks` should be flexible enough for creating other custom crawler tasks or running one-offs.

Since celerybeat is set up for this project, you could edit `hallofjustice/celeryconfig.py` to schedule a regular run that task periodically to monitor for missing or otherwise bad URLs.

### Admin

The admin has been customized with `cjdata/admin.py` and the grappelli package. There are probably a lot of things that can be done to improve the admin as curation of the data moves into the Django admin.

### Database

This project makes use of a number of PostgreSQL-specific features, such as Array and JSON fields. In addition, there a migration that enables the `intarray` extension (used getting items from the db by a set of ids in order) and another that creates a [GIN](http://www.postgresql.org/docs/9.4/interactive/gin.html) index on the *tags* arrayfield.

### CSV Export

The current implementation for exporting CSV streams an http response (see `common.views.CSVExportMixin`) so we can support export of custom searches as CSV. `search.views.SearchExportView` gets object ids from the haystack SearchQuerySet then performs a custom search to get results from the database in the search result order. This makes use of a PostgreSQL function from the included `intarray` extension.

There are views for exporting all Datasets or per category as CSV, and they should probably be lightly cached in production, or replaced with a periodic export. The export process does not transform arrayfields from their Django string representation (like `['NC', 'US']`), but that may be preferable to transforming values into some custom representation of the lists.