#!/usr/bin/env bash

apt-get -qq update
apt-get -qq install python2.7
apt-get -qq install postgresql libpq-dev
apt-get -qq install rabbitmq-server
apt-get -qq install python-virtualenv
apt-get -qq install git


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
