from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Song, User, Game
import random
from difflib import SequenceMatcher
import json

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
            songsPlayed = {}
            for song in Song.objects.all():
                songsPlayed[song.name] = [0,0] #format is: {song_name : [times_played, times_correct]}
            newUser.songs_played = json.dumps(songsPlayed)
            newUser.save()
            playerList.append(newUser)
        else:
            User.objects.get(name=request.POST[str(i)]).points = 0
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
        if request.POST['difficulty'] != '5':
            potentialSongs = list(Song.objects.filter(difficulty=int(request.POST['difficulty'])))
        else:
            potentialSongs = list(Song.objects.all())
        for j in range(int(request.POST['numRounds'])):
            print(len(potentialSongs))
            num = random.randrange(0, len(potentialSongs))
            song = potentialSongs.pop(num)
            songList.append(song)
            songListPK.append(song.pk)

    game.num_songs = len(songList)
    game.num_songs_per_player = len(songList)/len(playerList)
    game.song_list = songListPK
    game.save()

    context = {
        'songList' : songList,
        'playerList' : playerList,
    }

    return render(request, 'songQuiz/game.html', context)

def checkAnswer(request):

    userAnswer = request.POST['answer']
    game = Game.objects.order_by('-pk')[0]

    songListPK = game.song_list.strip("[']").split(", ")
    pk = songListPK.pop(0)
    song = Song.objects.get(pk=int(pk))
    answer = song.name

    playerList = []
    for i in range(len(game.players.strip("[']").split(", "))):
        playerList.append(User.objects.get(pk=int(game.players.strip("[']").split(", ")[i])))
    player = playerList[game.num_songs % game.num_songs_per_player - 1]

    songList = []
    for i in range(len(songListPK)):
        songListPK[i] = int(songListPK[i])
        songList.append(Song.objects.get(pk=songListPK[i]))

    game.song_list = songListPK
    game.save()

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
        player.points += song.points
        song.times_played += 1
        song.times_correct += 1
        tempDict = json.loads(player.songs_played)
        tempDict[song.name] = [tempDict[song.name][0]+1, tempDict[song.name][1]+1]
        player.songs_played = json.dumps(tempDict)
        player.save()
        song.save()
    else:
        print("wrong")
        song.times_played += 1
        tempDict = json.loads(player.songs_played)
        tempDict[song.name] = [tempDict[song.name][0]+1, tempDict[song.name][1]]
        player.songs_played = json.dumps(tempDict)
        player.save()
        song.save()

    #the following code may need to be moved so that there can be a screen in between that displays correct/wrong
    if len(songList) == 0:
        return HttpResponse("Results page placeholder.")
    else:
        context = {
            'songList' : songList,
            'playerList' : playerList,
        }

        return render(request, 'songQuiz/game.html', context)
