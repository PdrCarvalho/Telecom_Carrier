# pull official base image
FROM python:3.7.7-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL postgresql://db/postgres?user=postgres&password=postgres
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
# copy project
COPY . /usr/src/app/

WORKDIR /usr/src/app/

EXPOSE 5000

CMD  python /usr/src/app/manage.py db migrate;python manage.py db upgrade;python manage.py runserver --host 0.0.0.0