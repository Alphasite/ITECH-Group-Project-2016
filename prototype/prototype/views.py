from django.contrib.auth import authenticate, login, logout, get_user
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
import game.utility as user_util
from prototype import forms


# Create your views here.
class Register(View):
    # If it is a get, display the form for people to enter detail
    def get(self, request):
        form = forms.RegisterForm()
        return render(request, 'user/register.html', {'form': form})

    # Login otherwise
    def post(self, request):
        from game.models import UserProfile

        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            if user_util.check_exist(username, email):
                return HttpResponse('username or email already exists')
            else:
                user_util.save_user(username, password, email)
                # Direct to index page on success
                user = authenticate(username=username, password=password)

                profile = UserProfile(user=user)
                profile.save()

                login(request, user)
                return HttpResponseRedirect(reverse('game:index'))
        else:
            return user_util.json_response(-1, msg=form.errors)


class Login(View):
    # If it is a get, display the form for people to enter detail
    def get(self, request):
        form = forms.LoginForm()
        return render(request, 'user/login.html', {'form': form})

    # Login otherwise
    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('game:index'))
                else:
                    return user_util.json_response(-1, msg=u'The account is not activated, please contact administrator')
            else:
                return user_util.json_response(-1, msg=u'Username or password is incorrect')
        else:
            return user_util.json_response(-1, msg=form.errors)


class Logout(View):
    def get(self, request):
        logout(request)
        # redirect to site main page on success
        return HttpResponseRedirect(reverse('game:index'))


class UserProfile(View):
    def get(self, request):
        from game.models import UserProfile, Results

        # Fetch active game statistics
        profile = UserProfile.objects.get(user=get_user(request))
        game_states = profile.games

        has_active_game = False
        states_list = list()
        if len(game_states) > 0:
            has_active_game = True
            for game_state in game_states:
                states_list.append({
                    'theme': game_state.theme,
                    'balance': game_state.state.balance,
                    'score': game_state.state.score,
                    'last_played': game_state.state.last_played
                })

        # Fetch history best ranking
        ranking_zombuy = profile.best_ranking_zombuy
        ranking_foodshop = profile.best_ranking_foodshop

        context = {
            'has_active_game': has_active_game,
            'states_list': states_list,
            'ranking_zombuy': ranking_zombuy,
            'ranking_foodshop': ranking_foodshop
        }
        return render(request, 'profile/profile.html', context)
