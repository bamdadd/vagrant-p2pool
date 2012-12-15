# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.define :p2pool do |server|
    server.vm.box       = 'precise64'
    server.vm.box_url   = 'http://files.vagrantup.com/precise64.box'
    server.vm.host_name = 'p2poolvagrant'
    server.vm.forward_port 80, 8080
    server.vm.forward_port 9333, 9333
    server.vm.network :hostonly, "192.168.33.100"
  end
end
