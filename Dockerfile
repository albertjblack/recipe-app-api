# image we will build on top off
FROM python:3.9-alpine3.13 

# whoever is going to be maintaining docker image
LABEL maintainer="github.com/albertjblack"

# tells python we do not want to buffer output, we want to print output directly to console
ENV PYTHONUNBUFFERED 1

# cop y from local to out docker image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

# default directory that commands will run from .. location where dajngo project will be synced to
WORKDIR /app

# expose 8000 port of container running from our image
EXPOSE 8000

ARG ENV=false
# install dependencies "&& \" breaks commands into multiple lines
# create virtual environment for project so that base image dependencies do not conflict
# adduser .. not to use root user .. limited user .. no password cuz we will logon by default .. no hom .. name of user
RUN python -m venv /py && \
    # 
    /py/bin/pip install --upgrade pip && \ 
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV="true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \ 
    apk del .tmp-build-deps && \
    adduser \
    --disabled-password \ 
    --no-create-home \ 
    django-user

# update environment variable inside image so that we define that directory where executable can be run 
# whenever run python commands will not have to do /py/bin but can run directly
ENV PATH="/py/bin:$PATH"

# last line of dokcer file .. specify what user we are switching to .. everythin up is being done by root
USER django-user
