# Notes

Collecting notes on how to do some things with the project using ansible.


## Rebuild the search index

There is an ansible tag `rebuild_index` that is tied to the *rebuild search index* task in the **hallofjustice** role. Running `ansible-playbook` with the `rebuild_index` tag argument will trigger a rebuild of the search index, as run through Django's manage.py.

In your dev (Vagrant) environment, the command looks like:

```shell
ansible-playbook -i provisioning/hosts.vagrant provisioning/site.yaml -t rebuild_index -u vagrant --private-key=.vagrant/machines/site/virtualbox/private_key -vvvv
```
