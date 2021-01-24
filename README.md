# drf-adventures
Exploring Django Rest Framework features

## Setting up

    $ sudo apt install redis
    $ python3.8 -m venv venv
    $ source ./venv/bin/activate
    $ pip install -r requirements.txt
    $ python manage.py migrate

## Running

    $ python manage.py runserver
    $ celery -A drfadventures worker -l DEBUG
