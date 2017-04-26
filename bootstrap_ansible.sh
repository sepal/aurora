#!/usr/bin/env bash
#
# Bootstrap the vagrant VM by installing Ansible and
# letting ansible do the provisioning in local connection mode
#
version=$(ansible version 2>&1)

if echo "$version" | grep -q -i 'command not found'
then
  echo "[Vagrant] Ansible not found, installing.."

  sudo apt-get install software-properties-common
  sudo apt-add-repository ppa:ansible/ansible
  sudo apt-get update
  sudo apt-get -y install ansible
fi

echo 'localhost              ansible_connection=local' > /vagrant/hosts
PYTHONUNBUFFERED=1 ansible-playbook /vagrant/provision_vagrant_vm.yml -i /vagrant/hosts
