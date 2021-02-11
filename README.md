# drf-adventures
Exploring Django Rest Framework features

## Pre-reqs
    $ python3.8

## Setting up

    $ sudo apt update
    $ sudo apt install redis-server
    $ python3.8 -m venv venv
    $ source ./venv/bin/activate
    $ pip install -r requirements.txt
    $ python manage.py migrate

## Running

    $ python manage.py runserver
    $ celery -A drfadventures worker -l DEBUG

## Running Tests
    $ python3.8 manage.py test
