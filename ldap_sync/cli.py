#!/usr/bin/env python3

import sys
import logging
import argparse
import importlib

import requests

from ldap_sync.ldap import LDAP
from ldap_sync.source import bamboohr
from ldap_sync.config import Config
from ldap_sync.consts import DEFAULT_CONFIG_PATH, SOURCE_TYPES

logger = logging.getLogger(__name__)


def get_source(args):
    mod_name, cls_name = SOURCE_TYPES.get(args.source_type).split(':')
    mod = importlib.import_module(mod_name)
    source_cls = getattr(mod, cls_name)
    config = Config(args.config)
    return source_cls(config)


def sync(args):
    source = get_source(args)
    ldap = LDAP(args.dest)
    for user in source.get_user_data():
        ldap.add_user(user)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source-type', choices=SOURCE_TYPES.keys(), help='Source type of the HR system to sync from.')
    parser.add_argument('-d', '--dest', help='URL of the LDAP server to sync to.')
    parser.add_argument('-c', '--config', help='Path to the config file. (DEFAULT: %(default)s)',
                        default=DEFAULT_CONFIG_PATH)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s')

    sys.exit(sync(args))
