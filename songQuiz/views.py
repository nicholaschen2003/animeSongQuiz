from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Song, User, Game
import random
from difflib import SequenceMatcher
import json

def home(request):

    songs = list(Song.objects.order_by("percent_correct").reverse()[:4])
    print(songs)
    for i in range(len(songs)):
        songs[i] = "%s: %3.2f%%" % (songs[i].name, songs[i].percent_correct)

    print(songs)

    context = {
        'songs': songs,
    }

    return render(request, 'songQuiz/home.html', context)

def help(request):

    return render(request, 'songQuiz/help.html')

def getNumUsers(request):

    return render(request, 'songQuiz/getNumUsers.html')

def getPlayerData(request):

    context = {
        'numPlayers': request.POST['numUsers'],
        'numRounds': request.POST['numRounds']
    }

    return render(request, 'songQuiz/getPlayerData.html', context)

def createPlayers(request, numRounds):

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

    context = {
        'numRounds': numRounds
    }

    return render(request, 'songQuiz/getDifficulty.html', context)

def startGame(request, difficulty, numRounds):

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
        if str(difficulty) != '5':
            potentialSongs = list(Song.objects.filter(difficulty=int(difficulty)))
        else:
            potentialSongs = list(Song.objects.all())
        for j in range(int(numRounds)):
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
        'backgroundImagePath' : "/songQuiz/images/b"+str(random.randrange(1, 6))+".gif",
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
    print(game.num_songs_per_player)
    print(game.num_songs)
    print(len(playerList))
    print(((game.num_songs_per_player - (game.num_songs % game.num_songs_per_player)) -1) % len(playerList))
    player = playerList[((game.num_songs_per_player - (game.num_songs % game.num_songs_per_player)) - 1) % len(playerList)]

    songList = []
    for i in range(len(songListPK)):
        songListPK[i] = int(songListPK[i])
        songList.append(Song.objects.get(pk=songListPK[i]))

    game.song_list = songListPK
    game.num_songs = len(songList)
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
        player.points += song.points
        song.times_played += 1
        song.times_correct += 1
        song.percent_correct = round(float(song.times_correct) / song.times_played, 2)*100
        tempDict = json.loads(player.songs_played)
        tempDict[song.name] = [tempDict[song.name][0]+1, tempDict[song.name][1]+1]
        player.songs_played = json.dumps(tempDict)
        player.save()
        song.save()
        context = {
            'guess' : userAnswer,
            'points' : player.points,
        }
        return render(request, 'songQuiz/correct.html', context)

    else:
        song.times_played += 1
        song.percent_correct = round(float(song.times_correct) / song.times_played, 2)*100
        tempDict = json.loads(player.songs_played)
        tempDict[song.name] = [tempDict[song.name][0]+1, tempDict[song.name][1]]
        player.songs_played = json.dumps(tempDict)
        player.save()
        song.save()
        context = {
            'answer' : answer,
            'points' : player.points,
        }
        return render(request, 'songQuiz/wrong.html', context)

def continueGame(request):

    game = Game.objects.order_by('-pk')[0]
    playerListPK = game.players.strip("'[]").split(", ")
    playerList = []
    for i in range(len(playerListPK)):
        playerListPK[i] = int(playerListPK[i])
        player = User.objects.get(pk=playerListPK[i])
        playerList.append(player)
    songListPK = game.song_list.strip("'[]").split(", ")
    if songListPK == ['']:
        context = {
            'playerList' : list(User.objects.filter(pk__in=playerListPK).order_by("points").reverse()),
        }
        return render(request, 'songQuiz/results.html', context)

    else:
        songList = []
        for i in range(len(songListPK)):
            songListPK[i] = int(songListPK[i])
            song = Song.objects.get(pk=songListPK[i])
            songList.append(song)
        context = {
            'songList' : songList,
            'playerList' : playerList,
        }

        return render(request, 'songQuiz/game.html', context)

def clearPoints(request):
    game = Game.objects.order_by('-pk')[0]
    playerListPK = game.players.strip("'[]").split(", ")
    for playerPK in playerListPK:
        player = User.objects.get(pk=int(playerPK))
        player.points = 0
        player.save()

    return HttpResponseRedirect(reverse('songQuiz:home'))
