from django.contrib.auth.models import User
from django.db import models
from picklefield.fields import PickledObjectField
from game.simulation import engine


class GameState(models.Model):
    state = PickledObjectField()
    user = models.ForeignKey(User)
    theme = models.CharField(max_length=20)
    simulation_version = models.IntegerField(default=engine.VERSION)


class Results(models.Model):
    user = models.ForeignKey(User)
    score = models.IntegerField()
    theme = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)

    @property
    def games(self):
        return GameState.objects.filter(user=self.user)

    @property
    def results(self):
        return Results.objects.filter(user=self.user)
