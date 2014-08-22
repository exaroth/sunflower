#!/bin/bash

APP_NAME="sunflower"
DJANGO_DIR=/Users/konrad/Repositories/sunflower/sunflower
SOCKET_FILE=/Users/konrad/Repositories/sunflower/sunflower/run/gunicorn.sock
USER=konrad
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=sunflower.settings
DJANGO_WSGI_MODULE=sunflower.wsgi

echo "Running sunflower as `whoami`"

cd $DJANGO_DIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
RUNDIR=$(dirname $SOCKET_FILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec sudo ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
	--name $APP_NAME \
	--bind unix:$SOCKET_FILE \
	--workers $NUM_WORKERS \
	--log-level=debug

