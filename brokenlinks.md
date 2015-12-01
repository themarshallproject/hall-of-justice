
Broken Links = Broken Hearts

The following will walk you through the process of searching through the current list of URLs and identifying URLs that are broken or for some reason no longer functional. URLs are stored in a database, those URLs are then pulled out of the database and a http/get request is performed on the URL. If the server error is returned it is added to a list.


(This short guide assumes the project is setup and functioning properly, if it isn’t please see the readme)

vagrant up

vagrant ssh site

sudo su - hallofjustice#assumes the role and privileges of the hallofjustice user

cd src/hallofjustice #changes to the proper directory to run the remaining commands

python manage.py shell #enters the python shell

from cjdata.tasks import inspect_all_dataset_urls #imports the required function into the shell environment, afterwards the function can be run

from crawler import models # imports the models, models are how we access the data in the database which will be important later

inspect_all_dataset_urls() # runs function that calls to all the urls in the database and checks to make sure the links are still valid.

models.Crawl.objects.all() # returns all the existing crawls, when you run inspect_all_dataset_urls the count of crawls is incremented, remember the last number

exit() #exits the su user mode


Now we can output the broken links and start healing hearts.
There are two ways to do this.

python manage.py report_bad_links #(the number of the last crawl)

python manage.py report_bad_links #(the number of the last crawl) --output_file crawl5.csv

Example:
python manage.py report_bad_links 3 --output_file ../../brokenlinks.csv

#if you get a permission denied error you will probably need to go up a level to save the file (ex: ../../file.csv)

exit

mv /projects/hallofjustice/brokenlinks.csv /projects//hallofjustice/src/hallofjustice/.

The file should now be available on the local machine.
