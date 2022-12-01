FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN python manage.py makemigrations --noinput

RUN python manage.py migrate --noinput

RUN python manage.py createsuperuser --noinput --email mail@mail.com --username admin 

COPY . /app

ENTRYPOINT python manage.py runserver 0.0.0.0:8000
