from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from . import models

def listView(request):
    return render(request, 'app_meter/list.html')

def detailView(request):
    return render(request, 'app_meter/detail.html')

def createView(request):
    return render(request, 'app_meter/create.html')
