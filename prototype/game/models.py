from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField


# Create your models here.
class GameState(models.Model):
    current_time = PickledObjectField()
    event = models.OneToOneField("Event")
    user = models.ForeignKey(User)
    item = models.ForeignKey('Item')
    own_item = models.ForeignKey('OwnItem')


class Event(models.Model):
    time_to_execute = PickledObjectField()


class Results(models.Model):
    user = models.ForeignKey(User)
    score = PickledObjectField()


class Item(models.Model):
    name = models.CharField(max_length=20)
    price = models.ForeignKey('Price')


class Price(models.Model):
    price = PickledObjectField()
    time = PickledObjectField()


class OwnItem(models.Model):
    quantity = PickledObjectField()
    bought_price = PickledObjectField()
    item = models.OneToOneField(Item)




