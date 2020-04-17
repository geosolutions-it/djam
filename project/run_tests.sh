export DJAM_PROJECT_ENVIRONMENT=test
export DJAM_DB_NAME=
export DJAM_DB_USER=
export DJAM_DB_PASSWORD=
export DJAM_DB_HOST=
export DJAM_DB_PORT=

export DJAM_RABBITMQ_HOST=
export DJAM_RABBITMQ_PORT=

export DJAM_EMAIL_HOST=
export DJAM_EMAIL_SENDER=
export DJAM_EMAIL_HOST_USER=
export DJAM_EMAIL_HOST_PASSWORD=
export DJAM_EMAIL_PORT=

export DJAM_SECRET_KEY='#tm%3(w*8^3rt$3!9hgkdsvh8e*81h4p&ul*px@pg-!*j0-yd$'

coverage run --source='.' manage.py test
rm ../coverage.svg
coverage-badge -o ../coverage.svg
