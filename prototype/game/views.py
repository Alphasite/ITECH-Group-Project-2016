from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
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

class purchase(View):
    def get(self,request):
        #todo: do it with the real models
        sample_data =[
            {'quantity': '5','bought_price': '8','item': {'name' : 'spaghetti' ,'price':{'price':'5','time':'4'}}},
            {'quantity': '2','bought_price': '12','item': {'name' : 'toad' ,'price':{'price':'11','time':'4'}}},

            {'quantity': '77','bought_price': '31','item': {'name' : 'eeeeeeeeeeee' ,'price':{'price':'70','time':'4'}}},

            {'quantity': '1','bought_price': '1','item': {'name' : 'bread' ,'price':{'price':'2','time':'4'}}},

            {'quantity': '9','bought_price': '1','item': {'name' : 'probably' ,'price':{'price':'8','time':'4'}}}

        ]
        return render(request, 'game/purchase.html',{'sample_data': sample_data});