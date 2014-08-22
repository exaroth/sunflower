DJANGO_DIR=/Users/konrad/Repositories/sunflower/sunflower
DJANGO_SETTINGS_MODULE=sunflower.settings

cd $DJANGO_DIR

source ../bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec python manage.py runserver &

cd static
exec grunt 

