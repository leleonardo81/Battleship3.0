import os
# import django
from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Battleship.settings")
# django.setup()
app = get_channel_layer()