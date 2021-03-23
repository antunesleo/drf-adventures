FROM python:3.8

RUN apt-get update

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "thoughtsapi.wsgi", "--reload", "-c", "gunicorn.py"]