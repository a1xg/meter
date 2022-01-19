from django.forms import ModelForm
from . import models
# Написать форму создания счетчика
# форму загрузки показаний
# форму добавления ресурса и единиц измерения

class MeterForm(ModelForm):
    class Meta:
        model = models.Meter
        fields = '__all__'
