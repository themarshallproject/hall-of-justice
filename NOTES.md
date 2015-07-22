# Notes

Collecting notes on how to do some things with the project using ansible. Our development environment is set up as follows: Vagrant uses Ansible to configure virtual machines that are created using Virtualbox. These 3 tools (Vagrant, Ansible, Virtualbox) work together to create a development environment that closely mirrors the way things will be set up in production. The Ansible scripts should be usable to configure the servers needed to run the application in production.

## Getting a Vagrant environment

Getting your vagrant environment running should be fairly straightforward, as long as you have *Ansible*, *Virtualbox*, and *Vagrant* installed on your computer. The first step is to fetch the git submodules for this repo. So run:

```shell
hostcomputer:~$ git submodule init
hostcomputer:~$ git submodule updated
```

This should fetch the exact revision of *ansible-common-roles* this project depends on. The next step is to run:

```shell
hostcomputer:~$ vagrant up
```

This should take a few minutes as it creates and configures 4 virtual machines. **Sometimes, this will fail with errors.** I think this is some ansible/vagrant flakiness. If you end up with a machine that isn't fully configured, you can destroy a machine and rebuild it. So you could `vagrant destroy db` then `vagrant up db` to recreate the database virtual machine.


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

You should be able to view that instance of the site at http://10.73.98.100:9000. Now you can debug errors and view changes without having to mess with the default instance controlled by nginx and uwsgi.

## Restarting the default instance of the site

The default instance of the site at http://10.73.98.100/ is being served via [uwsgi](http://uwsgi-docs.readthedocs.org/en/latest/) and [nginx](http://nginx.org/en/), which is how the production version will run. You can use ansible to restart the default instance using the following:

```bash
hostcomputer:~$ ansible-playbook -i provisioning/hosts.vagrant provisioning/utils.yml -t website-restart -u vagrant --private-key=.vagrant/machines/site/virtualbox/private_key
```