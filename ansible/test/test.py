import pytest
import testinfra

@pytest.mark.parametrize("name", [
    "hostapd",
    "dnsmasq"
])
def test_package_is_installed(host, name):
    package = host.package(name)
    assert package.is_installed


@pytest.mark.parametrize("name", [
    "hostapd",
    "dnsmasq"
])
def test_daemons_are_installed(host, name):
    service = host.service(name)
    assert service.is_running
    assert service.is_enabled

#TODO
# Add test for proper folders creation
# Add test for iot_vpn_lab.services systemd (enabled and running)
    
# def test_iptables_nat_rules(host):
#     iptables = host.iptables("nat", )