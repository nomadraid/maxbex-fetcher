#!/bin/bash
# TimescaleDB schema initialisation

set -e

psql -w ${POSTGRES_PASSWORD} -d ${POSTGRES_DB} <<-EOSQL
    CREATE SCHEMA IF NOT EXISTS ${POSTGRES_SCHEMA}; 
EOSQL

exec "$@"