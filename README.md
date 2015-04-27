# hall-of-justice

Working with criminal justice data.

## Setup

*A work in progress. The set up will almost certainly change in the near future.*

You can take a properly formatted (fits the data schema) xlsx file and collapse it to a single csv using `scripts/collapse_xls_to_csv.py`. This csv can be imported into a Django database (already created using `python manage.py migrate`) using the *import_datasets* management command, i.e.: `python manage.py import_datasets /path/to/data.csv -v 3 2> import_errors.log`.

Once you've imported data into the database, you should create (or recreate) the elasticsearch search index using `python manage.py rebuild_index`.