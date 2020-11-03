# LDAP sync

Sync user data from a HR management system to a LDAP server.

## Installation

TODO: publish to pypi

```
pip install ldap_sync
```

## Usage

```
# edit the config
cp ldap_sync.cfg.example ldap_sync.cfg
vi ldap_sync.cfg

# run the command
ldap_sync -s bamboohr -d ldap://ldap.example.com -f ldap_sync.cfg
```

## Development

Note: the `Makefile` assumes you are using Debian/Ubuntu, if it's not the case, you need to install dependecies by yourself.

```
make
source venv/bin/activate
ldap_sync -h
```
