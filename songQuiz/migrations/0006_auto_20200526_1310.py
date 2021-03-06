# Generated by Django 3.0.3 on 2020-05-26 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songQuiz', '0005_auto_20200518_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='num_songs',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='num_songs_per_player',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='players',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='game',
            name='song_list',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='songs_played',
            field=models.TextField(default='{}'),
        ),
    ]
