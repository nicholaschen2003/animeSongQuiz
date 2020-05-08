from django.urls import path

from . import views

app_name = 'songQuiz'
urlpatterns = [
    path('', views.getNumUsers, name='getNumUsers'),
    path('getPlayerData/', views.getPlayerData, name='getPlayerData'),
    path('createPlayers/', views.createPlayers, name='createPlayers'),
]
