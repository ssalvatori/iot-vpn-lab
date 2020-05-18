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
    
# def test_iptables_nat_rules(host):
#     iptables = host.iptables("nat", )