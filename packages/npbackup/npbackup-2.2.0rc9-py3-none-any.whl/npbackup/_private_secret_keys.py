#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of npbackup

__intname__ = "npbackup.secret_keys"
__author__ = "Orsiris de Jong"
__copyright__ = "Copyright (C) 2023 NetInvent"
__license__ = "GPL-3.0-only"
__build__ = "2022120401"

# Encryption key to keep repo settings safe in plain text yaml config file
# Obtain a new key with:
# from cryptidy.symmetric_encryption import generate_key
# print(generate_key(32))

# This is the default key that comes with NPBackup... You should change it (and keep a backup copy in case you need to decrypt a config file data

#### WARNING: This is the NETPERFECT KEY, never publish on github

AES_KEY = (
    b"\xb7\xee\x8c8]\xde\xecsh[\xac\x84X1\xbf]3\xb1\xe5;W\x8d\x18oZ-\\ \xab\x8a\x82\xfb"
)
DEFAULT_BACKUP_ADMIN_PASSWORD = "netperfect_NPBACKUP00"
