# Transcendence project

[TODO. There will be project description]
```buildoutcfg
pip install -r requirements.txt
```

## Export environment variables
```
export DJANGO_SETTINGS_MODULE=transcendence.settings
export DJANGO_CONFIGURATION=Dev
export DJANGO_SECRET_KEY='your secret key'
```

## Create superuser
```buildoutcfg
(.venv)$ python3 manage.py createsuperuser
```
Here you should enter admin username and email
## Run server on localhost
```buildoutcfg
(.venv)$ python3 manage.py runserver --settings=transcendence.settings --configuration=Dev

```
## Add authorization module
```
$ python3 manage.py startapp auth
```
# Deploy fabfile
```

fab bootstrap:host=root@80.211.16.55

```
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
