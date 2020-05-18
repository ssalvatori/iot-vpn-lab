# Setup raspberry pi

## Install sshpass on mac
```
brew tap esolitos/ipa
brew install sshpass
```

### WiFI Configuration ( https://w1.fi/hostapd/ )

```
SSID_NAME
SSID_PASSPHARSE
SSID_COUNTRY_CODE
```

### NordVPN configuration
```
NORDVPN_USERNAME
NORDVPN_PASSWORD
```

## Run ansible
```
python3 -m venv venv
source venv/bin/activate
pip3 install ansible netaddr
ansible-playbook --user pi --ask-pass --inventory '192.168.0.150,' setup.yml
```
