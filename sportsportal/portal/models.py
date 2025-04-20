from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(default="default@example.com")
    team_name = models.CharField(max_length=100)
    game_name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user.username} - {self.team_name}"

class TeamManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100, unique=True)  # Ensures team name uniqueness
    game_name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user.username} - {self.team_name}"

class Guest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(default="default@example.com")
