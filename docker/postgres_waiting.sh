#!/bin/bash

set -e

host="$DB_HOST"
port="$DB_PORT"

until timeout 1 bash -c "echo > /dev/tcp/$host/$port"; do
  >&2 echo "Postgres is unavailable -> Booking sleeping"
  sleep 1
done

>&2 echo "Postgres is up -> Booking executing"
exec $@
