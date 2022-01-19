from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from . import models
from . import forms

def list_view(request):
    meters = models.Meter.objects.all()
    context = {'meters': meters}
    return render(request, 'app_meter/list.html', context)


def detail_view(request, pk):
    meter = models.Meter.objects.get(id=pk)
    print(f'meter: {meter}')
    records = models.Record.objects.filter(meter=pk)
    print(f'records: {records}')
    context = {
        'meter': meter,
        'records': records
    }

    return render(request, 'app_meter/detail.html', context)


def create_meter_view(request):
    error = ''
    if request.method == 'POST':
        form = forms.MeterForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            error = 'error'
    form = forms.MeterForm
    context = {
        'form':form,
        'error': error
    }

    return render(request, 'app_meter/create_meter.html', context)
