#!/usr/bin/env bash

set -o pipefail # trace ERR through pipes
set -o errexit

exec 6>&1
exec > /tmp/out.log


function fail { builtin echo "$@" 1>&2; }
function echo { builtin echo "$@" 1>&6; }
function printf { builtin printf "$@" 1>&6; }

function die {
    fail "$@"
    fail "FATAL ERROR! See /tmp/out.log for details."
    exit 1
}

function is_running { kill -0 $1 2> /dev/null; }

# Display a spinner until a process ends.
# Inspired by http://fitnr.com/showing-a-bash-spinner.html
function spinner {
    local pid=${1:?"pid is required"} fmt=${2-%s} erase=${3-"\b"}
    local delay=0.75 i=0 spinner=('|' '/' '-' '\')
    while is_running $pid; do
        printf "$fmt" ${spinner[i]}
        let i=(i+1)%4
        sleep $delay
        echo -ne $erase
    done
    echo -ne "     \b\b\b\b\b"
    wait $pid
}

function bgcommand {
    local pkg=$1
    shift
    echo -n "[    ] $pkg ... "
    eval $@ &
    spinner $! && echo -e "\r[ OK ]" || die -e "\r[FAIL] $pkg"
}

function postgres { su -c "$*" postgres; }
function sql { postgres "psql postgres -tAc \"$1\""; }



bgcommand "Running apt-get update" apt-get -qq update

for pkg in python2.7 python-dev postgresql libpq-dev rabbitmq-server \
           python-virtualenv git; do
    bgcommand "Installing $pkg" apt-get -qq install $pkg
done



if [[ $(sql "SELECT 1 FROM pg_roles WHERE rolname='vagrant'") != 1 ]]; then
    bgcommand "Creating postgres user: 'vagrant'" postgres createuser -DRS vagrant
fi

if [[ $(sql "SELECT 1 FROM pg_database WHERE datname='dash'") != 1 ]]; then
    bgcommand "Creating postgres database: 'dash'" postgres createdb dash
fi
