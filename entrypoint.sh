uwsgi --http 0.0.0.0:5000  --wsgi-file /app/app.py --callable app

# uwsgi --ini /app/uwsgi.ini