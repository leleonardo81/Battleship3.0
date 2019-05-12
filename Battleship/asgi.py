import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Battleship.settings")
django.setup()
app = get_default_application()