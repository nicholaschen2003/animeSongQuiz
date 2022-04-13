from django.db import models
import os

class Song(models.Model):
    name = models.CharField(max_length=200, default=None)
    file_path = models.CharField(max_length=200, default=None)
    difficulty = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    times_played = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
    percent_correct = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    def init():
        files = os.listdir("songQuiz/static/songQuiz/audio-final/")
        if ".DS_Store" in files:
            files.remove(".DS_Store")   #mac is dumb
        for filename in files:  #loops through song files
            #gets difficulty and "answer" for song
            difficulty, anime = filename.split("____")
            anime = anime.split("-")[0]
            #remove extraneous/irrelevant words
            if anime[-2:] == "TV" or anime[-2:] == "S1" or anime[-2:] == "S2" or anime[-2:] == "S3" or anime[-2:] == "S4" or anime[-2:] == "S5":
                anime = anime[:-2]
            if anime[-3:] == "OVA":
                anime = anime[:-3]
            try:
                test = int(anime[-4:])
                anime = anime[:-4]
            except:
                pass
            #create song object based on retrieved data
            newSong = Song(name=anime, file_path="songQuiz/audio-final/"+filename, difficulty=int(difficulty), points=int(difficulty)*100)
            newSong.save()

class User(models.Model):
    name = models.CharField(max_length=200, default=None)
    points = models.IntegerField(default=0)
    songs_played = models.TextField(default='{}') #also holds data on times played and times correct for each song played

    def __str__(self):
        return self.name

class Game(models.Model):
    num_songs_per_player = models.IntegerField(default=0)
    num_songs = models.IntegerField(default=0)
    players = models.TextField(default=None)
    song_list = models.TextField(default=None, null=True)

    def __str__(self):
        return self.players + "\n" + self.song_list
