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

    @property
    def best_ranking_zombuy(self):
        best_result = Results.objects.filter(user=self.user, theme='Zombuy').order_by('score')[:1]
        if len(best_result) == 0:
            return 'no history on Zombuy'
        else:
            # Get all the records that have better score than the user's best score
            better_results = Results.objects.filter(theme='Zombuy', score__gt=best_result[0].score)
            return len(better_results) + 1

    @property
    def best_ranking_foodshop(self):
        best_result = Results.objects.filter(user=self.user, theme='Foodshop').order_by('score')[:1]
        if len(best_result) == 0:
            return 'no history on Foodshop'
        else:
            # Get all the records that have better score than the user's best score
            better_results = Results.objects.filter(theme='Foodshop', score__gt=best_result[0].score)
            return len(better_results) + 1
