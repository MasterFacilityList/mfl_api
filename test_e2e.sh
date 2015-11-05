#!/usr/bin/env bash

set -e
set -o pipefail

function run_backend(){
    local err_log=$LOG_FOLDER/error.log
    local acc_log=$LOG_FOLDER/access.log

    if [[ ! -e "$LOG_FOLDER" ]]; then
        mkdir "$LOG_FOLDER"
    fi

    pip install --quiet -r requirements.txt
    cp .env-example .env
    wget "$DUMP_URL" -O mfl_dump.tar.gz --quiet
    tar xzf mfl_dump.tar.gz
    psql circle_test ubuntu -c "create extension if not exists postgis;" --quiet -o /dev/null
    psql circle_test ubuntu -c "create role mfl with password 'mfl' login superuser;" --quiet -o /dev/null
    psql circle_test ubuntu -c "create database mfl;" --quiet -o /dev/null
    psql mfl mfl -f mfl_dump.sql --quiet -o /dev/null
    python manage.py migrate -v0
    gunicorn -w 3 --timeout=300 --graceful-timeout=300 config.wsgi:application --bind=127.0.0.1:8061 --access-logfile "$acc_log" --error-logfile "$err_log" --log-level info --daemon

    cd $OLDPWD
}

function run_e2e(){
    local old_pwd="$OLDPWD"
    cd $HOME
    git clone --depth=1 --branch=master --quiet https://github.com/masterfacilitylist/mfl_admin_web
    cd mfl_admin_web
    npm install
    export PATH="$(npm bin):$PATH"
    grunt default
    nohup grunt connect:prod &
    npm run update-webdriver
    curl --retry 5 --retry-delay 2 -Lv http://localhost:8061 -o /dev/null
    grunt test:e2e
    killall --wait grunt
    cd $old_pwd
}

exit 0 # disable e2e for now until things stabilize

run_backend
run_e2e
