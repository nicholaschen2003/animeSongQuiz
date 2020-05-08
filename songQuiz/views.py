from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Song, User

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

    return HttpResponse("placeholder.")
