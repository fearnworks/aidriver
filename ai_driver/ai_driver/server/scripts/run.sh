#!/bin/bash

# Load environment variables from .env file
# set -a; source /.env; set +a

PRE_START_PATH=${PRE_START_PATH:-/app/prestart.sh}
echo "PRE_START_PATH is $PRE_START_PATH"
ls "$(dirname "$PRE_START_PATH")"

# If there's a prestart.sh script in the /app directory or other path specified, run it before starting
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi
# Add gunicorn logging configurations
export ACCESSLOG="-"  # '-' means log to stdout
export ERRORLOG="-"  # '-' means log to stderr
export LOGLEVEL="info"  # Set log level to info
# Run gunicorn
exec gunicorn --worker-tmp-dir /dev/shm --workers=6 \
    --bind $HOST:$PORT "$APP_MODULE" -k uvicorn.workers.UvicornWorker \
    --access-logfile $ACCESSLOG --error-logfile $ERRORLOG --log-level $LOGLEVEL --timeout $TIMEOUT\
