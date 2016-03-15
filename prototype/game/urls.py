from django.conf.urls import url

from game import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^top_table/?$', views.HighScoreTable.as_view(), name='high_score_table'),
    url(r'^games/(?P<game_id>\d+)/?', views.InProgressGame.as_view(), name='inprogress_game'),
    url(r'^games/(?P<theme_name>[\d\w-]+)', views.CreateGame.as_view(), name='create-game'),
]
