from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from game import views

urlpatterns = [
    url(r'^$', login_required(views.Index.as_view()), name='index'),
    url(r'^new_game/?$', login_required(views.NewGame.as_view()), name='new_game'),
    url(r'^top_table/?$', login_required(views.HighScoreTable.as_view()), name='high_score_table'),
    url(r'^games/(?P<game_id>\d+)/?', login_required(views.InProgressGame.as_view()), name='in-progress_games'),
]
