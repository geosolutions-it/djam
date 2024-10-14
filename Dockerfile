FROM python:3.10.15-slim
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get install gcc libpq-dev postgresql-15 postgresql-client-15 curl -y

RUN mkdir /djam
COPY ./requirements.txt /djam/requirements.txt

RUN pip3 install -r djam/requirements.txt && pip install uwsgi

COPY ./ /djam/

WORKDIR /djam/project

RUN  chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["sh", "docker-entrypoint.sh"]
