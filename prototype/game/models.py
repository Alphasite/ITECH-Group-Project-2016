from django.contrib.auth.models import User
from django.db import models
from picklefield.fields import PickledObjectField
from game.simulation import engine


class GameState(models.Model):
    # Rely on Django's Auto-Generated Primary Ket.
    state = PickledObjectField()
    user = models.ForeignKey(User)
    theme = models.CharField(max_length=20)
    simulation_version = models.IntegerField(default=engine.VERSION)


class Results(models.Model):
    user = models.ForeignKey(User)
    score = models.IntegerField()
    created = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)

    @property
    def games(self):
        return GameState.objects.get(user=User)

    @property
    def results(self):
        return Results.objects.get(user=User)
