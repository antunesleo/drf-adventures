# thoughts-api
Exploring Django Rest Framework features

## Pre-reqs
    $ python3.8
    $ sqlite

## Setting up Locally

    $ sudo apt update
    $ sudo apt install redis-server
    $ python3.8 -m venv venv
    $ source ./venv/bin/activate
    $ pip install -r requirements.txt
    $ python manage.py migrate

### Running

    $ python manage.py runserver
    $ celery -A thoughtsapi worker -l DEBUG

### Running Tests
    $ python3.8 manage.py test


## Setting up Docker

    $ docker-compose build
    $ docker-compose run web python manage.py migrate

### Running

    $ docker-compose up

### Running Test
    $ docker-compose run web python manage.py test

## API Usage

To show the API usecases the httpie tool will be used, but feel free to use another tool like curl.

### Create user account
`$ http POST http://127.0.0.1:8000/api/users/ first_name=Breno last_name=Brenilson email=breno@breno.com username=breno password=breno --json`

### Signin by JWT Authentication
`$ http POST http://127.0.0.1:8000/api/token username=breno password=breno --json`

### Refresh token (expires after 5 minutes)
`$ http POST http://127.0.0.1:8000/api/token/refresh refresh=YOUR_REFRESH_TOKEN --json`

### Publish a thought (requires access token)
 `$ http POST http://127.0.0.1:8000/api/thoughts thought="Como saci faz pra andar de patinete?" "Authorization: Bearer YOUR_ACCESS_TOKEN" --json`

### List user's thoughts
`$ http GET http://127.0.0.1:8000/api/thoughts?username=breno`

### Retrieve a thought
`$ http GET http://127.0.0.1:8000/api/thoughts/1/`
