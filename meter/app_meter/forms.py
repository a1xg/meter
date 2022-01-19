from django.forms import ModelForm
from . import models

# TODO написать форму загрузки показаний
# TODO написать форму добавления ресурса и единиц измерения


class MeterForm(ModelForm):
    class Meta:
        model = models.Meter
        fields = '__all__'
