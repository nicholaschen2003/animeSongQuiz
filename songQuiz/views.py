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
            playerList.append(User.objects.get(name=request.POST[str(i)]).pk)

    newGame = Game(players=playerList)
    newGame.save()

    return render(request, 'songQuiz/getDifficulty.html')

def startGame(request):

    game = Game.objects.order_by('-pk')[0]
    playerListPK = game.players.strip("'[]").split(", ")
    playerList = []
    for i in range(len(playerListPK)):
        playerListPK[i] = int(playerListPK[i])
        player = User.objects.get(pk=playerListPK[i])
        playerList.append(player)
    songList = []
    songListPK = []
    for i in range(len(playerList)):
        for j in range(int(request.POST['numRounds'])):
            if request.POST['difficulty'] != '5':
                potentialSongs = list(Song.objects.filter(difficulty=int(request.POST['difficulty'])))
                num = random.randrange(0, len(potentialSongs))
                song = potentialSongs.pop(num)
                songList.append(song)
                songListPK.append(song.pk)
            else:
                potentialSongs = list(Song.objects.all())
                num = random.randrange(0, len(potentialSongs))
                song = potentialSongs.pop(num)
                songList.append(song)
                songListPK.append(song.pk)

    game.song_list=songListPK
    game.save()

    context = {
        'songList' : songList,
        'playerList' : playerList,
    }

    return render(request, 'songQuiz/game.html', context)
