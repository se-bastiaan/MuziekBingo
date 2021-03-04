./manage.py collectstatic
./manage.py compress
gunicorn --bind=0.0.0.0 --timeout 600 bingo.wsgi