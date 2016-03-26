# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.define "app" do |app|

    app.vm.box = "centos/7"

    app.vm.network "forwarded_port", guest: 8080, host: 8080

    app.vm.network "private_network", ip: "192.168.100.111"
    app.vm.hostname = "app"

    app.vm.synced_folder ".", "/vagrant",
      :type => "nfs",
      :mount_options => ['nolock,vers=3,udp,noatime,actimeo=1']

  end

  config.vm.define "db" do |db|

    db.vm.box = "centos/7"

    db.vm.network "forwarded_port", guest: 3306, host: 3306

    db.vm.network "private_network", ip: "192.168.100.222"
    db.vm.hostname = "db"

  end

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 2048
    vb.cpus = 1
  end

end
