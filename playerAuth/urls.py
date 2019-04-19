from django.urls import path
from . import views

app_name = 'playerAuth'

urlpatterns = [
    path('', views.Login, name='login'),
    path('signup/', views.Signup, name='signup')
]