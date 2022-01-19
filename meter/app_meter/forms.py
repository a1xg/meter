from django.forms import ModelForm
from . import models

# TODO написать форму загрузки показаний
#  написать форму добавления ресурса и единиц измерения
#  форму загрузки CSV и логику для валидации


class MeterForm(ModelForm):
    class Meta:
        model = models.Meter
        fields = '__all__'


class UnitForm(ModelForm):
    class Meta:
        model = models.Unit
        fields = '__all__'


class ResourceForm(ModelForm):
    class Meta:
        model = models.Resource
        fields = '__all__'