vagrant-p2pool
==============

p2pool configurations with Vagrant and Puppet

install Ruby and RubyRVM before and then : puppet, Python, Vagrant, Fabric , VirtualBox

cd to the project directory and Run :

  vagrant up p2pool

* To check server is up : 

vagrant ssh p2pool
exit

* Install puppet on the VM :

fab vmp2pool bootstrap

* In order to Package files use :
./package.sh


