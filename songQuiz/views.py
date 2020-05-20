from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Song, User, Game
import random
from difflib import SequenceMatcher

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

    playerListPK = []

    for player in playerList:
        playerListPK.append(player.pk)

    newGame = Game(players=playerListPK)
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

    game.song_list = songListPK
    game.save()

    context = {
        'songList' : songList,
        'playerList' : playerList,
    }

    return render(request, 'songQuiz/game.html', context)

def checkAnswer(request):

    #get some POST data containing the user answer and check against correct answer
    #.remove the first song in game.song_list
    #check if length of song_list == 0
    #if true, display results page; else, render game.html
    userAnswer = request.POST['answer']
    game = Game.objects.order_by('-pk')[0]
    songListPK = game.song_list.strip("[']").split(", ")
    pk = songListPK.pop(0)
    song = Song.objects.get(pk=int(pk))
    answer = song.name
    #checks to see how much of the user answer matched with the answer
    correctPercent1 = 100*SequenceMatcher(None, answer.lower(), userAnswer.replace(" ","").lower()).ratio()
    correctPercent2 = 100*SequenceMatcher(None, userAnswer.replace(" ","").lower(), answer.lower()).ratio()
    #takes the larger percentage
    if correctPercent1 > correctPercent2:
        correctPercent = correctPercent1
    else:
        correctPercent = correctPercent2
    #if 70% or more of user answer matches with answer
    if correctPercent > 70:
        print("correct")
    else:
        print("wrong")

    songList = []
    for i in range(len(songListPK)):
        songListPK[i] = int(songListPK[i])
        songList.append(Song.objects.get(pk=songListPK[i]))

    game.song_list = songListPK
    game.save()

    if len(songList) == 0:
        return HttpResponse("Results page placeholder.")
    else:
        playerList = []
        for i in range(len(game.players.strip("[']").split(", "))):
            playerList.append(User.objects.get(pk=int(game.players.strip("[']").split(", ")[i])))

        context = {
            'songList' : songList,
            'playerList' : playerList,
        }

        return render(request, 'songQuiz/game.html', context)
