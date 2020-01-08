FROM python:3.7.4-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /djam
COPY ./ /djam/

RUN apk add --no-cache --virtual build-deps \
    postgresql-dev gcc musl-dev g++ linux-headers pcre pcre-dev \
    && pip install -r /djam/requirements.txt \
    && pip install uwsgi \
    && apk del build-deps

RUN apk add --no-cache postgresql
RUN apk add --no-cache pcre

WORKDIR /djam/project

RUN python manage.py migrate
RUN python manage.py collectstatic --no-input
CMD uwsgi --ini djam.ini & python manage.py rundramatiq
