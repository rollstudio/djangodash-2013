Vagrant::Config.run do |config|
  config.vm.define :djangovm do |config|
    # Every Vagrant virtual environment requires a box to build off of.
    config.vm.box = "precise32"
    config.vm.box_url = "http://files.vagrantup.com/precise32.box"

    # Forward a port from the guest to the host, which allows for outside
    # computers to access the VM, whereas host only networking does not.
    config.vm.forward_port 80, 8080
    config.vm.forward_port 8000, 8001

    config.vm.provision "puppet" do |puppet|
      puppet.module_path = "modules"
      puppet.manifests_path = "manifests"
      puppet.manifest_file = "site.pp"
    end
  end
end
