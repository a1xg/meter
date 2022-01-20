from django.shortcuts import render
from django.views.generic import UpdateView, CreateView, ListView, DetailView, DeleteView, FormView
from .services.data_processing import process_data, save_data
import pandas as pd
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
        return context


class ReadingsDeleteView(DeleteView):
    model = models.Readings
    success_url = '/'
    template_name = 'app_meter/readings_delete.html'

    def get_object(self, queryset=None):
        return models.Readings.objects.filter(meter=self.kwargs['pk'])

    def get_success_url(self):
        return f"/meter/{self.kwargs['pk']}"


class ReadingsFileFormView(FormView):
    form_class = forms.ReadingsFileForm
    template_name = 'app_meter/meter_detail.html'

    def get_success_url(self):
        return f"/meter/{self.kwargs['pk']}"

    def form_valid(self, form):
        form.check_file_type()
        # Подготавливаем CSV файл для записи
        df = process_data(csv_file=form.cleaned_data['csv_file'])
        save_data(df=df, meter_pk=self.kwargs['pk'])
        # находим существующие записи по конкретному счетчику
        exist_readings = models.Readings.objects.filter(meter=self.kwargs['pk'])

        return super().form_valid(form)



# TODO написать вьюхи для добавления единиц измерения и ресурсов, для загрузки CSV
class CreateUnit(CreateView):
    model = models.Unit
    form_class = forms.UnitForm


class CreateResource(CreateView):
    model = models.Resource
    form_class = forms.ResourceForm