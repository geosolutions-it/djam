python -W ignore manage.py collectstatic -c --noinput
python -W ignore manage.py migrate --noinput
python -W ignore manage.py creatersakey
echo "running dramatiq"
nohup python manage.py rundramatiq &
echo "running django"
python manage.py runserver 0.0.0.0:8000