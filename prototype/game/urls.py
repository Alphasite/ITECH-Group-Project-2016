from django.conf.urls import patterns
from django.conf.urls import url

from game import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_game/?$', name='new_game'),
    url(r'^$', views.index, name='register')
]
