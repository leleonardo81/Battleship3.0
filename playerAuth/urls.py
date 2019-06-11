from django.urls import path, include
from . import views

app_name = 'playerAuth'

urlpatterns = [
    path('', views.Login, name='login'),
    path('signup/', views.Signup, name='signup'),
    path('google-login/', views.google_login, name='glogin'),
    path('logout/', views.loggedout, name='logout')
]