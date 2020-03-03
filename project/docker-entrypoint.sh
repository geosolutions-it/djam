python -W ignore manage.py collectstatic -c --noinput
python -W ignore manage.py migrate --noinput
python -W ignore manage.py creatersakey
uwsgi --ini djam.ini & python manage.py rundramatiq
