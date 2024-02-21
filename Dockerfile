FROM python:3.10.4-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /djam
COPY ./ /djam/

RUN apk add --no-cache --virtual build-deps \
    postgresql-dev gcc musl-dev g++ linux-headers pcre pcre-dev curl \
    && pip install -r /djam/requirements.txt \
    && pip install uwsgi \
    && apk del build-deps

RUN apk add --no-cache postgresql
RUN apk add --no-cache pcre
RUN pip3 install -r djam/requirements-dev.txt
WORKDIR /djam/project

RUN  chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["sh", "docker-entrypoint.sh"]
