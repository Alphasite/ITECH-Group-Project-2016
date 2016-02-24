from django.shortcuts import render
from django.views.generic import View


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

        context = {
            'users_score_zombuy': users_score_zombuy,
            'users_score_foodshop': users_score_foodshop,
        }

        return render(request, 'highscore/table.html', context)
