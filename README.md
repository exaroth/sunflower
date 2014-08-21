# Sunflower

![](sunflower_thumb.jpg)

Sunflower is a simple image gallery written in Django framework. It strives to
be easy to use and focus on presenting content in a clear and distraction free fashion.


## Installation

This assumes you're working in a virtualenv for deployment

### Setting up the project

Create new virtualenv folder

```shell
virtualenv <project_name>
```

Activate it:

```shell
# from withing <project_name> folder
source bin/activate
```

Clone sunflower repository:

```shell
git clone https://github.com/exaroth/sunflower.git
```

Lastly install all the requirements:

```shell
# from within sunflower folder
pip install -r requirements.txt
```

### Running the app

* Edit `settings.py` file, change `DEBUG` to `False`

* (Optional) Install memcached and run it on port 11211:

```shell
memcached -d -p 11211
```

Note Sunflower will still run even without memcached but the content won't be cached (d'oh).
