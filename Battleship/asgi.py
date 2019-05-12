import os
# import django
import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Battleship.settings")
# django.setup()
app = channels.asgi.get_channel_layer()