from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField


# Create your models here.
class GameState(models.Model):
    current_time = PickledObjectField()
    event = models.OneToOneField(Event)
    user = models.ManyToOneRel(User)
    item = models.ManyToOneRel(Item)
    own_item = models.ManyToOneRel(OwnItem)


class Event(models.Model):
    time_to_execute = PickledObjectField()


class Results(models.Model):
    user = models.ForeignKey(User)
    score = PickledObjectField()


class Item(models.Model):
    name = models.CharField(max_length=20)
    price = models.ManyToOneRel(Price)


class Price(models.Model):
    price = PickledObjectField()
    time = PickledObjectField()


class OwnItem(models.Model):
    quantity = PickledObjectField()
    bought_price = PickledObjectField()
    item = models.OneToOneField(Item)




