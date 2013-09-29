#!/usr/bin/env bash

apt-get update
apt-get install -y postgresql libpq-dev
apt-get install -y rabbitmq-server
apt-get install -y python-virtualenv

function postgres {
    su -c "$*" postgres
}

function sql {
    postgres "psql postgres -tAc \"$1\""
}

sql "SELECT 1 FROM pg_roles WHERE rolname='vagrant'" | grep -q 1 || 
    postgres createuser -DRS vagrant

sql "SELECT 1 FROM pg_database WHERE datname='dash'" | grep -q 1 ||
    postgres createdb dash

cd /vagrant
rm -rf .h
mkdir .h
cd .h
mkdir logs cookiecutters cookiecutters_out
virtualenv env
source env/bin/activate
pip install -r ../requirements/base.txt

