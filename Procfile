release: python manage.py migrate
web: gunicorn Battleship.asgi:channel_layer
worker: python manage.py runworker -v2