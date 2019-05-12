release: python manage.py migrate
web: daphne Battleship.asgi:app --port $8000 --bind 0.0.0.0
worker: python manage.py runworker