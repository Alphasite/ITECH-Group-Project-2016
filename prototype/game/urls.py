from django.conf.urls import url

from game import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^new_game/?$', views.create_game, name='new_game'),
    url(r'^$', views.register, name='register'),
]
