import json

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

from game.themes import themes
from game.models import Results


class Index(View):
    def get(self, request):
        return render(request, 'index/body.html')


class HighScoreTable(View):
    def get(self, request):

        results_zombuy = Results.objects.filter(theme='Zombuy').order_by('-score')[:5]
        users_score_zombuy = list()

        for result_zombuy in results_zombuy:
            users_score_zombuy.append({
                'username': result_zombuy.user.username,
                'score': result_zombuy.score,
            })

        results_foodshop = Results.objects.filter(theme='Foodshop').order_by('-score')[:5]
        users_score_foodshop = list()
        for result_foodshop in results_foodshop:
            users_score_foodshop.append({
                'username': result_foodshop.user.username,
                'score': result_foodshop.score,
            })

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

        if state.time < state.theme.time_limit:
            state.tick()

            persist.state = state
            persist.save()

            state = {
                "success": True,
                "gameover": False,
                "next": reverse("game:inprogress_game", kwargs={"game_id": game_id})
            }

        else:
            state = {
                "success": True,
                "gameover": True,
                "next": reverse("game:gameover", kwargs={"game_id": game_id})
            }

        return HttpResponse(json.dumps(state), status=200, content_type="application/json")


class GameOver(View):
    @method_decorator(login_required)
    def get(self, request, game_id):
        from game.models import GameState, Results
        try:
            result = Results.objects.get(id=game_id)
        except Results.DoesNotExist:
            game = GameState.objects.get(id=game_id)
            state = game.state

            result = Results(id=game.id, user=request.user, score=state.score, theme=game.theme)
            result.save()

            game.delete()

        context = {
            "score": result.score,
            "theme": result.theme,
        }

        return render(request, "gameover/gameover.html", context)


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
