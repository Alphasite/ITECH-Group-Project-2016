from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from models import Item

class Index(View):
    def get(self, request):
        return render(request, 'index/body.html')


class NewGame(View):
    def get(self, request):
        return render(request, 'game/game.html')


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

    # @method_decorator(login_required)
    def get(self, request, game_id):
        game_state = {
            "balance": 100,
            "days_remaining": 7,
        }
        return render(request, 'game/game.html', {'state': game_state})

    def put(self, request):
        pass

class graphView(View):

    def get(self, request):
        items = {'name': "hello", 'price':[{'price': 20, 'time':1},{'price': 40, 'time':2}, {'price': 0, 'time':0}]}
        return render(request, 'game/graph.html', {'items':items})