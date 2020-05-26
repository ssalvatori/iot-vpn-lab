Vagrant.configure(2) do |config|

  config.vm.box = "gvfoster/raspbian"
  
  config.vm.hostname = "iot-lab"
  config.vm.provider "virtualbox" do |v|
    v.name = "iot-lab"
    v.memory = 2048
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install virtualenv build-essential python3-dev libdbus-glib-1-dev libgirepository1.0-dev libssl-dev sshpass -y
    python3 -m venv /tmp/venv
    source /tmp/venv/bin/activate
    pip3 install wheel 
    pip3 install ansible==2.9.9 netaddr
    cd /vagrant/ansible

    export SSID_NAME=vpn-test
    export SSID_PASSPHARSE=test
    export SSID_COUNTRY_CODE=de
    export NORDVPN_USERNAME=user
    export NORDVPN_PASSWORD=password
    export AWS_ATS_ENDPOINT=http://localhost
    export AWS_THING_NAME=iot-test
    export ANSIBLE_HOST_KEY_CHECKING=False
    ansible-playbook -i inventory/vagrant setup.yml
  SHELL

end
