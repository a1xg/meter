from django.shortcuts import render
from django.views.generic import UpdateView, CreateView, ListView, DetailView, DeleteView
from . import models
from . import forms


class CreateMeterView(CreateView):
    model = models.Meter
    form_class = forms.MeterForm
    template_name = 'app_meter/meter_create_update.html'


class UpdateMeterView(UpdateView):
    model = models.Meter
    form_class = forms.MeterForm
    template_name = 'app_meter/meter_create_update.html'


class DeleteMeterView(DeleteView):
    model = models.Meter
    success_url = '/'
    template_name = 'app_meter/meter_delete.html'


class ListMetersView(ListView):
    model = models.Meter
    context_object_name = 'meters'
    template_name = 'app_meter/meters_list.html'


class DetailMeterView(DetailView):
    queryset = models.Meter.objects.all()
    context_object_name = 'meter'
    template_name = 'app_meter/meter_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['readings'] = models.Readings.objects.filter(meter=self.object)
        print(context)
        return context


# TODO написать вьюхи для добавления единиц измерения и ресурсов, для загрузки CSV
class CreateUnit(CreateView):
    model = models.Unit
    form_class = forms.UnitForm


class CreateResource(CreateView):
    model = models.Resource
    form_class = forms.ResourceForm