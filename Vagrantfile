# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|


  config.vm.box = "chef/ubuntu-14.04"

  config.vm.define "db" do |db|
    db.vm.network "private_network", ip: "10.73.98.101"
    db.vm.provider "virtualbox" do |vb|
      vb.name = "db.hallofjustice"
      vb.memory = 1024
    end

    db.vm.provision "ansible" do |ansible|
      ansible.playbook = "provisioning/db.yaml"
      ansible.inventory_path = "provisioning/hosts.vagrant"
      ansible.limit = "all"
      ansible.extra_vars = { deploy_type: "vagrant" }
      ansible.raw_arguments = ["-T 30"]
    end
  end

  config.vm.define "search" do |search|
    search.vm.network "private_network", ip: "10.73.98.102"
    search.vm.provider "virtualbox" do |vb|
      vb.name = "search.hallofjustice"
      vb.memory = 1024
    end

    search.vm.provision "ansible" do |ansible|
      ansible.playbook = "provisioning/search.yaml"
      ansible.inventory_path = "provisioning/hosts.vagrant"
      ansible.limit = "all"
      ansible.extra_vars = { deploy_type: "vagrant" }
      ansible.raw_arguments = ["-T 30"]
    end
  end

  config.vm.define "site" do |site|
    site.vm.network "private_network", ip: "10.73.98.100"
    site.vm.synced_folder "./", "/projects/hallofjustice/src/hallofjustice"
    site.vm.provider "virtualbox" do |vb|
      vb.name = "site.hallofjustice"
    end

    site.vm.provision "ansible" do |ansible|
      ansible.playbook = "provisioning/site.yaml"
      ansible.inventory_path = "provisioning/hosts.vagrant"
      ansible.limit = "all"
      ansible.extra_vars = { deploy_type: "vagrant" }
      ansible.raw_arguments = ["-T 30"]
    end
  end

end
