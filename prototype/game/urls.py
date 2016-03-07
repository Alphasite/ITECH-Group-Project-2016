from django.conf.urls import url

from game import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^new_game/?$', views.NewGame.as_view(), name='new_game'),
    url(r'^top_table/?$', views.HighScoreTable.as_view(), name='high_score_table'),
    url(r'^games/(?P<game_id>\d+)/?', views.InProgressGame.as_view(), name='in-progress_games'),
    url(r'^purchase/?$', views.purchase.as_view(),name='purchase')
]
