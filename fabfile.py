from __future__ import with_statement
from fabric.api import *
import fabric.contrib.project as project
from fabric.context_managers import shell_env
import os
from django.conf import settings as django_settings
import ConfigParser
from contextlib import contextmanager


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sunflower.settings")
config = ConfigParser.ConfigParser()
config.readfp(open("sunflower.cfg"))

base_cfg = config._sections["main"]
gunicorn_cfg = config._sections["gunicorn"]

env.user = "user"
env.hosts = ["localhost",]
env.directory = os.path.realpath(os.path.join(django_settings.ROOT_DIR, os.pardir))
env.activate = 'source {0}'.format(env.directory + "/bin/activate")

@contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

def grunt_dev_server():
    local("cd static && grunt")

def django_test_server():
    with virtualenv():
        local("python manage.py runserver")

def run_dev():
    grunt_dev_server()
    django_test_server()
