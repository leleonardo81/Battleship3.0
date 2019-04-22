release: python manage.py migrate
web: daphne Battleship.asgi:channel_layer
worker: python manage.py runworker -v2