python -W ignore manage.py collectstatic -c --noinput
python -W ignore manage.py migrate --noinput
python -W ignore manage.py creatersakey
echo "running dramatiq"
nohup python manage.py rundramatiq &
echo "running django"
cd /djam/project
DJANGO_SETTINGS_MODULE=settings gunicorn wsgi --bind=0.0.0.0:8000