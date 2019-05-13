release: python manage.py migrate
web: bin/start-pgbouncer daphne Battleship.asgi:app --port $PORT --bind 0.0.0.0
worker: python manage.py runworker