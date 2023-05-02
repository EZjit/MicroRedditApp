# base image
FROM python:3.11-alpine3.17
# creator email
LABEL maintainer='weinbloodlust@gmail.com'
# setup environment variable - project directory
#ENV DockerHOME=/home/app/microreddit

# set work directory
#RUN #mkdir -p $DockerHOME
#WORKDIR $DockerHOME
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# upgrade pip package manager
RUN pip install --upgrade pip

# copy whole project to your docker home directory.
#COPY . $DockerHOME
COPY . /app
# install all dependencies and create non-root user
RUN pip install -r requirements.txt && \
    adduser --disabled-password --no-create-home app
# port where the Django app runs
#EXPOSE 8000
# change user
USER app
# start server
#CMD python manage.py runserver 0.0.0.0:8000