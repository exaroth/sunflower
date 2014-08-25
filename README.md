# Sunflower

![](sunflower_thumb.jpg)

Sunflower is a simple image gallery written in Django framework. It strives to
be easy to use and focus on presenting content in a clear and distraction-free fashion.

You can see working example under [konradwasowicz.com/sunflower](konradwasowicz.com/sunflower)


## Installation

This assumes you're using `virtualenv` for deployment

### Setting up the project

* Create new virtualenv folder
```shell
virtualenv <project_name>
```

* Activate it:
```shell
# from within <project_name> folder
source bin/activate
```

* Clone sunflower repository:
```shell
git clone https://github.com/exaroth/sunflower.git
```

* Lastly install all the requirements:
```shell
# from within sunflower folder
pip install -r requirements.txt
```

* (Optional) Install memcached and run it on port 11211:
```shell
# for mac users
brew install memcached
```
```shell
# for linux users
sudo apt-get install memcached
```
Then run it:
```shell
memcached -d -p 11211
```

**Note:** Sunflower will still run even without memcached but the content won't be cached (d'oh).

### Running development server

* Inside `/static/` directory execute `npm install && bower install` to download required Javascript libraries.

* Configure database settings inside `settings.py` file and execute `python manage.py syncdb` to create required tables.

* Then edit `run_dev_server.sh` file and change `DJANGO_DIR` to an absolute path to your project (the directory with `manage.py` file).


* Execute `run_dev_server.sh`:
```shell
./run_dev_server.sh
```
This will start django dev server along with grunt and will compile less and refresh browser each time you make any changes to html, js or less files.


### Running production server

This assumes you're using Nginx as a http server and Gunicorn as WSGI one.
* Install gunicorn inside virtualenv and add it to `INSTALLED_APPS` in settings.py
* **IMPORTANT** Change `SECRET_KEY` value to anything you like.
* Add your hostname into `ALLOWED_HOSTS` list
* Define database backend inside `settings.py` - see [relevant entry](https://docs.djangoproject.com/en/dev/ref/databases/) in Django documentation for details.
* Execute `python manage.py syncdb`.
* Go to `static/` folder and execute `grunt build` if you have made any changes to css or javascript, this will compile, concatenate and minify all the required files.
* Edit `run_sunflower.sh` script, inside you will find following variables (starred entries should be changed):
    + `APP_NAME` - name of the application
    + *`DJANGO_DIR` - absolute path to the project
	+ *`USER` - define user account gunicorn process will be running as (preferably `www-data`)
    + *`SOCKET_FILE` - absolute path to unix socket file to be used with `bind` flag when running gunicorn server
    + `NUM_WORKERS` - number of workers to be used by gunicorn
    + `DJANGO_SETTINGS_MODULE` - string denoting settings.py module inside the app
    + `DJANGO_WSGI_MODULE` - same as above but for wsgi module


* Then configure Nginx server to use gunicorn as reverse proxy. You can find example configuration that works fairly well in [Gunicorn documentation](http://gunicorn-docs.readthedocs.org/en/latest/deploy.html). Be sure to add proper aliases for `static` and `media` directories as files inside are served straight from hdd.
* Finally run memcached, execute `run_sunflower.sh` and restart Nginx with new configuration and you're set to go.

## Software used:

* [Django](https://github.com/django/django)
* [Django-imagekit](https://github.com/django/django)
* [Salvattore](https://github.com/rnmp/salvattore)
* [Jquery](https://github.com/jquery/jquery)
