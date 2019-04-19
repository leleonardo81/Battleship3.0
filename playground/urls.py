from django.urls import path
from . import views

app_name = 'playground'

urlpatterns = [
    path('', views.index, name='index'),
    path('join/', views.join, name='join'),
    path('room/<int:room_id>/', views.room, name='room'),
    path('create/', views.create, name='create')

]