from django.shortcuts import render
from django.views.generic import View
import forms


class Index(View):
    def get(self, request):
        return render(request, 'index/body.html')


# def register(request):
#     registered = False
#     if request.method == 'POST':
#
#         user_form = forms.UserForm(data=request.POST)
#         if user_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             registered = True
#
#         else:
#             print user_form.errors
#
#     else:
#         user_form = forms.UserForm()
#
#     return render(request, 'common/base.html', {'user_form': user_form, 'registered': registered})
