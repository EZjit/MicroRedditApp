# base image
FROM python:3.11-alpine3.17
# creator email
LABEL maintainer='weinbloodlust@gmail.com'

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# upgrade pip package manager
RUN pip install --upgrade pip

# copy whole project to your docker home directory.
COPY . /app
# install all dependencies and create non-root user
RUN pip install -r requirements.txt && \
    adduser --disabled-password --no-create-home app

# change user
USER app