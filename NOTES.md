# Notes

Collecting notes on how to do some things with the project using ansible.


## Rebuild the search index

There is an ansible tag `rebuild_index` that is tied to the *rebuild search index* task in the **hallofjustice** role. Running `ansible-playbook` with the `rebuild_index` tag argument will trigger a rebuild of the search index, as run through Django's manage.py.

In your dev (Vagrant) environment, the command looks like:

```shell
ansible-playbook -i provisioning/hosts.vagrant provisioning/site.yml -t rebuild_index -u vagrant --private-key=.vagrant/machines/site/virtualbox/private_key
```

## Interacting with the database

You should be able to: `psql -h 10.73.98.101 -U hallofjustice -d hallofjustice` and enter `test` for the password to log into the Vagrant machine database from your host machine.

## Running in DEBUG mode with Vagrant machines

From the vagrant "hallofjustice-site" machine, you can switch to the application account and run a server with DEBUG=True set in the environment (other env vars are automagically loaded via that account's .bashrc). Essentially:

```bash
hostcomputer:~$ vagrant ssh site
vagrant@hallofjustice:~$ sudo su - hallofjustice
(virt)hallofjustice@hallofjustice:~$ cd src/hallofjustice/
(virt)hallofjustice@hallofjustice:~/src/hallofjustice$ export DEBUG=True
(virt)hallofjustice@hallofjustice:~/src/hallofjustice$ ./manage.py runserver 0.0.0.0:9000
```

Now you can debug errors and view changes without having to mess with the instance controlled by nginx and uwsgi.