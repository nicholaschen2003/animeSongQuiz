from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'songQuiz'
urlpatterns = [
    path('', views.home, name='home'),
    path('help/', views.help, name='help'),
    path('getNumUsers/', views.getNumUsers, name='getNumUsers'),
    path('getPlayerData/', views.getPlayerData, name='getPlayerData'),
    path('createPlayers/<int:numRounds>', views.createPlayers, name='createPlayers'),
    path('startGame/<int:difficulty>/<int:numRounds>/', views.startGame, name='startGame'),
    path('checkAnswer/', views.checkAnswer, name='checkAnswer'),
    path('continueGame/', views.continueGame, name='continueGame'),
    path('clearPoints/', views.clearPoints, name='clearPoints'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
