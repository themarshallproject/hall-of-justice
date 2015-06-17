# hall-of-justice

Working with criminal justice data.

## Setup

*A work in progress. The set up will almost certainly change in the near future.*

You can take a properly formatted (fits the data schema) xlsx file and collapse it to a single csv using `scripts/collapse_xls_to_csv.py`. This csv can be imported into a Django database (already created using `python manage.py migrate`) using the *import_datasets* management command, i.e.: `python manage.py import_datasets /path/to/data.csv -v 3 2> import_errors.log`.

You can look for errors around datasets that failed to import (`grep '^Failed to save dataset' import_errors.log | sort`) or categories that don't exist (`grep category$ import_errors.log | uniq | sort`). There are also  rows from the csv where there wasn't enough data to create a dataset (*Not enough data to create a dataset!*), but those are likely mostly empty rows from the input csv.

Once you've imported data into the database, you should create (or recreate) the elasticsearch search index using `python manage.py rebuild_index`.