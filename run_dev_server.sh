#!/bin/bash
DJANGO_DIR=/Users/konrad/Repositories/sunflower/sunflower
DJANGO_SETTINGS_MODULE=sunflower.settings

cd $DJANGO_DIR

source ../bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export DJANGO_DEBUG_VAR=1

exec python manage.py runserver &

cd static
exec grunt 

