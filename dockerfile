FROM python:3.7.7-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

WORKDIR /usr/src/app/

# CMD  python /usr/src/app/manage.py db migrate;python manage.py db upgrade;python manage.py runserver --host 0.0.0.0