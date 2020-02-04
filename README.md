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

export DJAM_DB_NAME=...        (default=djam)
export DJAM_DB_USER=...        (default=djam)
export DJAM_DB_PASSWORD=...    (default=djam)
export DJAM_DB_HOST=...        (default=localhost)
export DJAM_DB_PORT=...        (default=5432)

export DJAM_RABBITMQ_HOST=...  (default=localhost)
export DJAM_RABBITMQ_PORT=...  (default=5672)
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

## Side notes

* To properly read data from Token Info endpoint the client has to have `token_introspection` and their ID present in the available scopes (/admin -> Clients model -> Scopes) 
* OpenId Provider defines additional scope `user_id` for accessing User's database ID. This feature usage should be as limited as possible, for now it is present for Allauth simple integration.
* To integrate certain Geoserver flows: `/roles`, `/users`, and `adminRole` endpoint access is required. These endpoints are protected with API key, which should be passed as Authorization header in a format: `apiKey {key}`.
Generating API key can be done in the admin page -> `API KEY PERMISSIONS` -> `API keys` -> `Add` 

## Running the tests

No tests are yet preapared

## Deployment

The easiest deployment strategy is to create a docker container using Dockerfile from the main project directory. Docker container sets up uWSGI server (which connects with `http-socket = :8000`) along with `python manage.py rundramatiq` command.

Remember to properly set configuration, especially DJAM_DB_HOST and DJAM_RABBITMQ_HOST when running the dockerized aplication.

* Build docker image: `docker build . -t djam`
* Start docker container: `docker run -e DJAM_DB_HOST=192.168.x.x -e DJAM_RABBITMQ_HOST=192.168.x.x -p 8000:8000 djam`

The container sets up a uWSGI server along with dramatiq
On the start of the docker container `python manage.py collectstatic` and `python manage.py migrate` commands are performed.

Static files have to be served separately using e.g. Nginx. The static files are located in `/djam/project/static` container directory.

##### Postgres with Docker deployment

When setting up Postgresql, make sure proper permissions are set to access the database from docker.
You have to check pg_hba.conf and postgresql.conf files.

For Postgres on the host machine:
* pg_hba.conf -> add a row for docker0 address from `ip a`
* postgresql.conf -> uncomment line and allow all, or just specific listen_addresses `listen_addresses = '*'`

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/geosolutions-it/djam/tags). 

## Geoserver integration

##### Openid authentication
To be able to use Djam based authentication from Geoserver a recent build of geonode-oauth2 extension is required, because [this commit](https://github.com/geoserver/geoserver/commit/6e6ef47ce2bee359a705ce25c58fd8088f90417f) is required.

##### Auth-key authentication and authorization
Geoserver integration is possible also by AuthKey ([see documentation](https://docs.geoserver.org/stable/en/user/community/authkey/index.html)).
AuthKey is returned in the OpenID Code response along with ID and Access tokens, labelled as `session_token`.
Geoserver configuration for this authentication and authorization method:
* Login to Geoserver with admin privileges
* `Security` -> `Settings`: make sure Active role service is `default` (to prevent doubled checks for privileges in different Roles services)
* `Security` -> `Users, Groups, Roles`: `Add new` Role Service with the following parameters:
    * `AuthKEY REST` - Role service from REST endpoint
    * name: `djam_roleservice`
    * Base Server URL: `http://your-djam-domain`
    * Roles REST Endpoint: `/api/privilege/geoserver/roles`
    * Admin Role REST Endpoint: `/api/privilege/geoserver/adminRole`
    * Users REST Endpoint: `/api/privilege/geoserver/users` [note: this endpoint won't be used in this integration]
    * Roles JSON Path: `$.groups`
    * Admin Role JSON Path: `$.adminRole`
    * Users JSON Path: `$.users[?(@.username=='${username}')].groups`
    * REST Rules Cache Concurrency Level: `4`
    * REST Rules Cache Maximum Size (# keys): `10000`
    * REST Rules Cache Expiration Time (ms): `30000`
* `Security` -> `Users, Groups, Roles`: `Add new` User Group Service with the following parameters:
    * `AuthKEY WebService Body Response` - UserGroup Service from WebService Response Body
    * name: `djam_groupservice`
    * Password encryption: `Empty`
    * Password policy: `default`
    * Web Service Response Roles Search Regular Expression: `^.*?"groups"\s*:\s*\["([^"]+)"\].*$`
    * Optional static comma-separated list of available Groups from the Web Service response: leave this empty
    * Role Service to use (empty value means: use the current Active Role Service): `djam_roleservice`
* `Security` -> `Authentication`: `Add new` Authentication Filter with the following parameters:
    * `AuthKey` - Authenticates by looking up for an authentication key sent as URL parameter
    * name: `djam_filter`
    * name of URL parameter: `authkey`
    * Authentication key to user mapper: `Web Service`
    * Web Service URL, with key placeholder: `http://your-djam-domain/openid/authkey/introspect/?authkey={key}&format=json`
    * Web Service Response User Search Regular Expression: `^.*?\"username\"\s*:\s*\"([^\"]+)\".*$`
    * User/Group Service: `djam_groupservice`
* `Security` -> `Authentication` -> `Filter Chains`:
    * `web` -> `Chain filters`: move `djam_filter` for "available" to "selected" column, ABOVE `anonymous` filter and press Close
    * `default` -> `Chain filters`: move `djam_filter` for "available" to "selected" column, ABOVE `anonymous` filter and press Close
    * **Remember** to press `Save` at the bottom of the `Authentication` page, otherwise the settings won't be applied!

From now on you can authenticate your requests to Geoserver by attaching `authkey` parameter to a querystring, e.g. 
`http://your-domain/geoserver/geonode/wms?service=WMS&...&authkey=84fb7e8d-9642-4ec7-b8e3-a6447ad1c709`.
