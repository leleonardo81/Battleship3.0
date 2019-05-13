release: python manage.py migrate
web: daphne Battleship.asgi:app --port $PORT --bind 0.0.0.0
worker: python manage.py runworker