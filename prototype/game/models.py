from django.db import models
from django.contrib.auth import models as auth_model


# Create your models here.

# class Slang(models.Model):
#     user = models.ForeignKey(auth_model.User)
#     word = models.CharField(max_length=10)
#     definition = models.CharField(max_length=1000)
#     example = models.CharField(max_length=1000)
#     trending_score = models.IntegerField()
#     date_added = models.DateField()


# class Comments(models.Model):
#     user = models.ForeignKey(auth_model.User)
#     slang = models.ForeignKey(Slang)
#     score = models.IntegerField()
#     comment = models.CharField(max_length=1000)
#     definition = models.CharField(max_length=1000)
#     date_added = models.DateField()
