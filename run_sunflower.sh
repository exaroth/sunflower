#!/bin/bash

APP_NAME="sunflower"
DJANGO_DIR=/path/to/project/dir
SOCKET_FILE=/path/to/socket/file
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=sunflower.settings
DJANGO_WSGI_MODULE=sunflower.wsgi
USER=konrad
LOG_FILE=/dev/null

echo "Running sunflower as `whoami`"

cd $DJANGO_DIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export DJANGO_DEBUG_VAR=0
RUNDIR=$(dirname $SOCKET_FILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
	--name $APP_NAME \
	--user $USER \
	--bind unix:$SOCKET_FILE \
	--workers $NUM_WORKERS \
	--log-level=debug \
	--log-file=$LOG_FILE

