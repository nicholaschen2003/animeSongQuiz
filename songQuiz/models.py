from django.db import models

class Song(models.Model):
    name = models.CharField(max_length=200, default=None)
    file_path = models.CharField(max_length=200, default=None)
    difficulty = models.CharField(max_length=200, default=None)
    points = models.IntegerField(default=0)
    times_played = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=200, default=None)
    points = models.IntegerField(default=0)
    songs_played = models.CharField(max_length=1000, default=None) #also holds data on times played and times correct for each song played

    def __str__(self):
        return self.name
