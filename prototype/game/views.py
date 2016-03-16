import json

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

from game.simulation.engine import State
from game.themes import themes


class Index(View):
    def get(self, request):
        return render(request, 'index/body.html')

class HighScoreTable(View):
    def get(self, request):
        users_score_zombuy = [
            {'username': 'nishad', 'score': 66666},
            {'username': 'gerry', 'score': 28374},
            {'username': 'euan', 'score': 100},
            {'username': 'vincent', 'score': -9}
        ]

        users_score_foodshop = [
            {'username': 'vincent', 'score': 28374},
            {'username': 'euan', 'score': 2374},
            {'username': 'gerry', 'score': 999},
            {'username': 'nishad', 'score': 44}
        ]

        themes = [
            {'name': 'Zombuy', 'scores': users_score_zombuy},
            {'name': 'Foodshop', 'scores': users_score_foodshop}
        ]

        return render(request, 'highscore/table.html', {'themes': themes})


class InProgressGame(View):
    @method_decorator(login_required)
    def get(self, request, game_id):
        from game.models import GameState

        persist = GameState.objects.get(id=game_id)
        state = persist.state

        if persist is not None:
            return render(request, 'game/game.html', {
                'state': persist.state,
                'items': persist.state.items,
            })
        else:
            HttpResponse(status=404)

    @method_decorator(login_required)
    def post(self, request, game_id):
        from game.models import GameState

        persist = GameState.objects.get(id=game_id)
        state = persist.state

        data = json.loads(request.body)

        for item in state.items:
            item.owned = int(data[item.name])

        state.tick()

        persist.state = state
        persist.save()

        return HttpResponse(status=200)



class CreateGame(View):
    @method_decorator(login_required)
    def post(self, request, theme_name):
        from game.models import GameState

        if theme_name in themes:
            state = GameState()
            state.user = request.user
            state.state = themes[theme_name].simulation
            state.theme = theme_name
            state.save()

            return HttpResponseRedirect(reverse('game:inprogress_game', kwargs={'game_id': state.id}))
        else:
            return HttpResponse(status=422)
