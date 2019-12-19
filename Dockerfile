FROM python:3.7.4-alpine
ENV PYTHONUNBUFFERED 1
ENV DJAM_PROJECT_ENVIRONMENT dev

RUN mkdir /djam
COPY ./ /djam/

#RUN \
# apt get --no-cache postgresql-libs && \
# apt get --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
# python3 -m pip install -r requirements.txt --no-cache-dir && \
# apt --purge del .build-deps

#RUN apt-get update -y && apt-get install -y postgresql-dev gcc python3-dev musl-dev

#RUN apt-get install libpq-dev

#RUN apt-get -y remove libsqlite3-dev xz-utils liblzma-dev



RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r /djam/requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


#RUN pip install -r /djam/requirements.txt
#RUN pip install --upgrade pip && pip install --no-cache-dir -r /djam/requirements.txt

WORKDIR /djam/project

CMD python manage.py runserver 0.0.0.0:8000
