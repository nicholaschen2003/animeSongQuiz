from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'songQuiz'
urlpatterns = [
    path('', views.getNumUsers, name='getNumUsers'),
    path('getPlayerData/', views.getPlayerData, name='getPlayerData'),
    path('createPlayers/', views.createPlayers, name='createPlayers'),
    path('startGame/', views.startGame, name='startGame'),
    path('checkAnswer/', views.checkAnswer, name='checkAnswer'),
    path('continueGame/', views.continueGame, name='continueGame'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
