Vagrant::Config.run do |config|
  config.vm.define :djangovm do |django_config|
    # Every Vagrant virtual environment requires a box to build off of.
    django_config.vm.box = "precise32"
    django_config.vm.box_url = "http://files.vagrantup.com/precise32.box"

    # Forward a port from the guest to the host, which allows for outside
    # computers to access the VM, whereas host only networking does not.
    django_config.vm.forward_port 80, 8080
    django_config.vm.forward_port 8000, 8001

    django_config.vm.provision :shell, :inline => "echo hello!"
    django_config.vm.provision :shell, :path => "etc/install.sh"
  end
end
