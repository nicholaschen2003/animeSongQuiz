from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Song, User, Game
import random

def getNumUsers(request):

    return render(request, 'songQuiz/getNumUsers.html')

def getPlayerData(request):

    context = {
        'numPlayers': request.POST['numUsers']
    }

    return render(request, 'songQuiz/getPlayerData.html', context)

def createPlayers(request):

    playerList = []
    for i in range(1, len(request.POST)):
        if request.POST[str(i)] not in User.objects.values_list('name', flat=True):
            newUser = User(name=request.POST[str(i)])
            newUser.save()
            playerList.append(newUser)
        else:
            playerList.append(User.objects.get(name=request.POST[str(i)]))

    context = {
        'playerList' : str(playerList),
    }

    return render(request, 'songQuiz/getDifficulty.html', context)

def startGame(request, playerList):

    playerList = playerList.strip('][').split(', ')
    songList = []
    for i in range(len(playerList)):
        for j in range(int(request.POST['numRounds'])):
            if request.POST['difficulty'] != '5':
                potentialSongs = list(Song.objects.filter(difficulty=int(request.POST['difficulty'])))
                num = random.randrange(0, len(potentialSongs))
                songList.append(potentialSongs.pop(num))
            else:
                potentialSongs = list(Song.objects.all())
                num = random.randrange(0, len(potentialSongs))
                songList.append(potentialSongs.pop(num))

    newGame = Game(players=str(playerList), song_list=str(songList))
    newGame.save()
    
    return HttpResponse("placeholder.")
