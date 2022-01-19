from django.shortcuts import render
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from django.http import HttpResponse, HttpResponseNotFound
from . import models
from . import forms


class CreateMeterView(CreateView):
    template_name = 'app_meter/create_meter.html'
    model = models.Meter
    form_class = forms.MeterForm


class ListMetersView(ListView):
    model = models.Meter
    context_object_name = 'meters'
    template_name = 'app_meter/list.html'


class DetailMeterView(DetailView):
    queryset = models.Meter.objects.all()
    context_object_name = 'meter'
    template_name = 'app_meter/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['records'] = models.Record.objects.filter(meter=self.object)
        return context

