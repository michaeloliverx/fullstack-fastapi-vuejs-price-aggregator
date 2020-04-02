#!/bin/sh

set -e

# wait for our database to be ready
dockerize -wait "tcp://$POSTGRES_HOST:$POSTGRES_PORT" -timeout 10s


# add waiting for other services here


# activate our virtual environment to ensure
# poetry commands are ran against it
. /opt/pysetup/.venv/bin/activate

# Evaluating passed command:
exec "$@"