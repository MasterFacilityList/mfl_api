#!/usr/bin/env python

from django.db import connection
from django.core.mail import mail_admins
from celery.schedules import crontab
from celery.decorators import periodic_task

from fabfile import backup_mfl_db


@periodic_task(
    run_every=(crontab(minute=0, hour='*/1')),
    name="backup_db",
    ignore_result=True)
def backup_db():
    """
    Backup the MFL database

    Creates a backup file for the MFL db, zips and ships
    it to amazon S3 every day at midnight
    """

    try:
        backup_mfl_db()
    except:
        mail_admins(
            subject="MFL Database backup Error",
            message="An error has occurred while taking the MFL database "
            "backup . Please investigate the issue"
        )


@periodic_task(
    run_every=(crontab(minute='*/10')),
    name="refresh_material_views",
    ignore_result=True)
def refresh_material_views():
    """
    Refresh material views.

    There is need to refresh the facilities materialized view every
    time facility metadata changes. Hook the refreshes here.

    The the task will be running after every 10 minutes
    """

    sql = """refresh materialized view facilities_excel_export;"""
    cursor = connection.cursor()
    cursor.execute(sql)
