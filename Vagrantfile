# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "centos/7"

  config.vm.network "forwarded_port", guest: 8080, host: 8080

  config.vm.network "private_network", ip: "192.168.50.6"

  config.vm.synced_folder ".", "/vagrant",
    :type => "nfs",
    :mount_options => ['nolock,vers=3,udp,noatime,actimeo=1']

  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    vb.memory = 2048
    vb.cpus = 4
  end

end
