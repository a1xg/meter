from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from . import models


def list_view(request):
    return render(request, 'app_meter/list.html')


def detail_view(request):
    return render(request, 'app_meter/detail.html')


def create_view(request):
    return render(request, 'app_meter/create.html')
