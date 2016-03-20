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
        from game.models import UserProfile

        profile = UserProfile.objects.get(user=get_user(request))
        states = profile.games

        in_progress = True
        score_zombuy = 'Not in any active game'
        ranking_zombuy = 'Not in any active game'
        score_foodshop = 'Not in any active game'
        ranking_foodshop = 'Not in any active game'

        if len(states) > 0:
            for state in states:
                print state.theme
                if state.theme == 'Zombuy':
                    score_zombuy = state.state.score
                    # Get the ranking
                    ranking_zombuy = 1
                elif state.theme == 'Foodshop':
                    score_foodshop = state.state.score
                    ranking_foodshop = 1

        context = {
            'in_progress': in_progress,
            'balance': 50,
            'score_zombuy': score_zombuy,
            'ranking_zombuy': ranking_zombuy,
            'score_foodshop': score_foodshop,
            'ranking_foodshop': ranking_foodshop,
        }
        return render(request, 'profile/profile.html', context)
