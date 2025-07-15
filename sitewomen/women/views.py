from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    for i in request:
        print(i)
    return HttpResponse("Страница приложения women.")


def categories(request):
    return HttpResponse("<h1>Статьи по категориям</h1>")
