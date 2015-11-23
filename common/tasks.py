#!/usr/bin/env python
"""
Backup the MFL database

Creates a backup file for the MFL db, zips and ships
it to amazon S3 every day at midnight
"""

from django.core.mail import mail_admins
from celery.schedules import crontab
from celery.decorators import periodic_task

from fabfile import backup_mfl_db


@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="backup_db",
    ignore_result=True)
def backup_db():
    try:
        backup_mfl_db()
    except:
        mail_admins(
            subject="MFL Database backup Error",
            message="An error has occurred while taking the MFL database "
            "backup . Please investigate the issue"
        )
