# DJAM
Django Access Management, implementing OpenID Identity Provider and custom Privilege Management System

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* An SMTP email server
* Python 3.8+ (tested in Python 3.10)
* PostgreSQL 11.0+
* RabbitMQ 3.8+

The environment dependencies can be installed in dockerized version, e.g for RabbitMQ:

```
docker run -d -p 15672:15672 -p 5672:5672 -p 5671:5671 --hostname localhost rabbitmq:3-management
```

### Installation

Clone git repository

```
git clone git@github.com:geosolutions-it/djam.git
```

Create environment configuration for Djam. Make sure DJAM_PROJECT_ENVIRONMENT is set to 'local',
 to set DEBUG mode and not to require ALLOWED_HOSTS definitions.

To create the environment configuratino for DJAM create an .env file in the root directory: DJAM>>.env and include the confituration there. An example of the .env file is presented below:

```
DJAM_PROJECT_ENVIRONMENT=local
DJAM_RABBITMQ_HOST=...  (default=localhost)
DJAM_RABBITMQ_PORT=...  (default=5672)
DJAM_DB_HOST=<DB host e.g 127.0.0.1>
DJAM_DB_PORT=...  (default=5432)
DJAM_DB_NAME=<djam db>
DJAM_DB_USER=<djam user>
DJAM_DB_PASSWORD=<db password>
DJAM_EMAIL_HOST=...
DJAM_EMAIL_PORT=...
DJAM_EMAIL_HOST_USER=...
DJAM_EMAIL_HOST_PASSWORD=...
APIKEY_EXPIRE_DAYS=... (The expiration timedelta of the keys in days. The default value is 30)
```
Afterwards, from the root folder of the DJAM repository, run the following command to prepare the environment:

```bash
set -a && . ./.env && set +
```

Create virtualenv in djam directory

```bash
python3 -m venv venv
```

Activate virtualenv, install requirements and navigate to project source dir

```bash
source venv/bin/activate
pip install -r requirements.txt
cd project
```

Optionally run project checks, to see if everything is as expected. If any errors occur correct them before continuation.

```bash
python manage.py check
```

Migrate your app

```bash
python manage.py migrate
```

Create your app's superuser

```bash
python manage.py createsuperuser
```

Create your OpenID provider a pair of private - public keys

```bash
python manage.py creatersakey
```

Run dramatiq queue - this process should be active for the whole application lifetime

```bash
python manage.py rundramatiq
```

For development purposes - in a new terminal start django dev server

```bash
python manage.py runserver 0.0.0.0:8000
```

From now on you can start working with your application. To add OpenID client navigate to `http://localhost:8000/admin`
and in OPENID CONNECT PROVIDER add row to Clients table.

You can also check User registration form at `http://localhost:8000/register`. REMEMBER: to register the User
you first need update `djam/project/conf/local/email.py` configuration file with SMTP server credentials.   

## API Documentation - Swagger

To create the corresponding schema.yml for the API documentation (Swagger) run the following command:

```bash
python manage.py spectacular --color --file schema.yml
```
Afterwards, Swagger front-end should exist in the following URL: `http://localhost:8000/openid/api/schema/swagger-ui/`

## Side notes

* To properly read data from Token Info endpoint the client has to have `token_introspection` and their ID present in the available scopes (/admin -> Clients model -> Scopes) 
* OpenId Provider defines additional scope `user_id` for accessing User's database ID. This feature usage should be as limited as possible, for now it is present for Allauth simple integration.
* To integrate certain Geoserver flows: `/roles`, `/users`, and `adminRole` endpoint access is required. These endpoints are protected with API key, which should be passed as Authorization header in a format: `apiKey {key}`.
Generating API key can be done in the admin page -> `API KEY PERMISSIONS` -> `API keys` -> `Add` 

## Running the tests

In the `project` folder simply run:

`./run_tests.sh`

To generate a html report simply run:

`coverage html`

And to view something like:

`firefox htmlcov/index.html`

To regenerate the coverage badge, simply run this in the project folder:

`coverage-badge -o ../coverage.svg`

## Deployment

The easiest deployment strategy is to create a docker container using Dockerfile from the main project directory. Docker container sets up uWSGI server (which connects with `http-socket = :8000`) along with `python manage.py rundramatiq` command.

Remember to properly set configuration, especially DJAM_DB_HOST and DJAM_RABBITMQ_HOST when running the dockerized aplication.

* Build docker image: `docker build . -t djam`
* Start docker container: `docker run -e DJAM_DB_HOST=192.168.x.x -e DJAM_RABBITMQ_HOST=192.168.x.x -p 8000:8000 djam`

The container sets up a uWSGI server along with dramatiq
On the start of the docker container `python manage.py collectstatic` and `python manage.py migrate` commands are performed.

Static files have to be served separately using e.g. Nginx. The static files are located in `/djam/project/static` container directory.

### Postgres with Docker deployment

When setting up Postgresql, make sure proper permissions are set to access the database from docker.
You have to check pg_hba.conf and postgresql.conf files.

For Postgres on the host machine:

* pg_hba.conf -> add a row for docker0 address from `ip a`
* postgresql.conf -> uncomment line and allow all, or just specific listen_addresses `listen_addresses = '*'`

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/geosolutions-it/djam/tags). 

## Linting Setup

As a prerequisite in your virtualenv run `pip install -r requirements-dev.txt`

## Running the linters

`flake8 project/`
`bandit project/`

### Vscode Integration

In your settings.json:

```json
{
    "python.pythonPath": "venv/bin/python",
    "python.linting.flake8Path": "venv/bin/flake8",
    "python.linting.banditPath": "venv/bin/bandit",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.banditEnabled": true,
}
```

