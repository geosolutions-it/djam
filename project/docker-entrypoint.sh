python -W ignore manage.py collectstatic --noinput
python -W ignore manage.py migrate --noinput
python -W ignore manage.py loaddata example_admin --noinput
python -W ignore manage.py creatersakey
echo "running dramatiq"
nohup python manage.py rundramatiq -p 1 -t 1  &
echo "running django"
cd /djam/project

if [ "$DJAM_PROJECT_ENVIRONMENT" == "dev" ]; then
    python manage.py runserver 0.0.0.0:8000
else
  DJANGO_SETTINGS_MODULE=settings gunicorn wsgi --bind=0.0.0.0:8000
fi