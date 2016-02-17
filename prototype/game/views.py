from django.shortcuts import render
from game.forms import UserForm

def index(request):
    return render(request, 'index/body.html')


def logout(request):
    return ""

def register(request):
    registered = False
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True

        else:
            print user_form.errors

    else:
        user_form = UserForm()


    return render(request,
            'common/base.html',
            {'user_form': user_form, 'registered': registered} )