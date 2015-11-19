#!/usr/bin/env python

"""
Creates a backup file for the mfl db, zips and sends
it over for storage at S3
"""

from fabfile import backup_mfl_db

backup_mfl_db()
