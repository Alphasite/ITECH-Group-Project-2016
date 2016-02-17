from django.shortcuts import render


def index(request):
    return render(request, 'index/body.html')


def register(request):
    return ""


def logout(request):
    return ""
