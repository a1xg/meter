from django.views import generic
from .services.readings_service import ReadingsProcessor
from . import models
from . import forms


class CreateMeterView(generic.CreateView):
    model = models.Meter
    form_class = forms.MeterForm
    template_name = 'app_meter/meter_create_update.html'


class UpdateMeterView(generic.UpdateView):
    model = models.Meter
    form_class = forms.MeterForm
    template_name = 'app_meter/meter_create_update.html'


class DeleteMeterView(generic.DeleteView):
    model = models.Meter
    success_url = '/'
    template_name = 'app_meter/meter_delete.html'


class ListMetersView(generic.ListView):
    model = models.Meter
    context_object_name = 'meters'
    template_name = 'app_meter/meters_list.html'


class DetailMeterView(generic.DetailView):
    queryset = models.Meter.objects.all()
    context_object_name = 'meter'
    template_name = 'app_meter/meter_detail.html'

    def get_context_data(self, **kwargs):
        context = super(generic.DetailView, self).get_context_data(**kwargs)
        context['readings'] = models.Readings.objects.filter(meter=self.object)
        return context


class ReadingsDeleteView(generic.DeleteView):
    model = models.Readings
    success_url = '/'
    template_name = 'app_meter/readings_delete.html'

    def get_object(self, queryset=None):
        return models.Readings.objects.filter(meter=self.kwargs['pk'])

    def get_success_url(self):
        return f"/meter/{self.kwargs['pk']}"


class ReadingsFileFormView(generic.FormView):
    form_class = forms.ReadingsFileForm
    template_name = 'app_meter/meter_detail.html'

    def get_success_url(self):
        return f"/meter/{self.kwargs['pk']}"

    def form_valid(self, form):
        form.check_file_type()
        processor = ReadingsProcessor(
            csv_file=form.cleaned_data['csv_file'],
            meter_pk=self.kwargs['pk']
        )
        processor.save_data()

        return super().form_valid(form)


# TODO написать вьюхи для добавления единиц измерения и ресурсов
class CreateUnitView(generic.CreateView):
    model = models.Unit
    form_class = forms.UnitForm
    success_url = '/meter/create'
    template_name = 'app_meter/resource_unit_add.html'

    def get_context_data(self, **kwargs):
        form = self.get_form()
        return {
            'title': 'Create new unit',
            'form': form
        }


class CreateResourceView(generic.CreateView):
    model = models.Resource
    form_class = forms.ResourceForm
    success_url = '/meter/create'
    template_name = 'app_meter/resource_unit_add.html'

    def get_context_data(self, **kwargs):
        form = self.get_form()
        return {
            'title': 'Create new resource',
            'form': form
            }
