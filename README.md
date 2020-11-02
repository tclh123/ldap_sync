# LDAP sync

Sync user data from a HR management system to a LDAP server.

## Installation

TODO:

```
pip install ldap_sync

ldap_sync -s bamboohr -d ldap://ldap.example.com
```

## Development

Note: the `Makefile` assumes you are using Debian/Ubuntu, if it's not the case, you need to install dependecies by yourself.

```
make
source venv/bin/activate
ldap_sync -h
```
