# djam
Django Access Management, implementing OpenID Identity Provider and custom Privilege Management System

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* An SMTP email server
* Python 3.7 with:
    * Django 3.0+
    * Dramatiq 1.7+
    * psycopg2 2.8+
* PostgreSQL 11.0+
* RabbitMQ 3.8+

The environment dependencies can be installed in dockerized version, e.g for RabbitMQ:

```
docker run -d -p 15672:15672 -p 5672:5672 -p 5671:5671 --hostname my-rabbitmq rabbitmq:3-management
```

### Installing

Clone git repository

```
git clone git@github.com:geosolutions-it/djam.git
```

Create environment configuration for Djam. Make sure DJAM_PROJECT_ENVIRONMENT is set to 'dev',
 to set DEBUG mode and not to require ALLOWED_HOSTS definitions

```
export DJAM_PROJECT_ENVIRONMENT=dev

export DJAM_DB_NAME=...
export DJAM_DB_USER=...
export DJAM_DB_PASSWORD=...
export DJAM_DB_HOST=...
export DJAM_DB_PORT=...

export DJAM_RABBITMQ_HOST=...
```

Create virtualenv in djam directory

```
python3.7 -m venv venv
```

Activate virtualenv, install requirements and navigate to project source dir

```
source venv/bin/activate
pip install -r requirements.txt
cd project
```

Migrate your app

```
python manage.py migrate
```

Create your app's superuser

```
python manage.py createsuperuser
```


Create your OpenID provider a pair of private - public keys

```
python manage.py creatersakey
```

Run dramatiq queue - this process should be active for the whole application lifetime

```
python manage.py rundramatiq
```

For development purposes - in a new terminal start django dev server

```
python manage.py runserver 0.0.0.0:8000
```

From now on you can start working with your application. To add OpenID client navigate to `http://localhost:8000/admin`
and in OPENID CONNECT PROVIDER add row to Clients table.

You can also check User registration form at `http://localhost:8000/register`. REMEMBER: to register the User
you first need update `djam/project/conf/dev/email.py` configuration file with SMTP server credentials.   

## Running the tests

No tests are yet preapared

## Deployment

Dockerfile in preparation

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/geosolutions-it/djam/tags). 
