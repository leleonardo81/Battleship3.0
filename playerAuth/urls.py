from django.urls import path, include
from . import views

app_name = 'playerAuth'

urlpatterns = [
    path('', views.Login, name='login'),
    path('signup/', views.Signup, name='signup'),
    # path('google-login/', include('social_django.urls', namespace='social')),
]