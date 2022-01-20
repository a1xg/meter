import io
import csv
from django.forms import ModelForm, Form, FileField, ValidationError
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


class ReadingsFileForm(Form):
    csv_file = FileField()

    def clean_data_file(self):
        """Checking the file type"""
        file = self.cleaned_data['csv_file']
        if file:
            ext = file.name.split('.')[-1]
            if ext != 'csv':
                raise ValidationError('File Type not supported')
            return file

    def process_data(self):
        # TODO написать валидацию и бизнес логику
        print(f'FORM{self.cleaned_data}')
        file = io.TextIOWrapper(self.cleaned_data['csv_file'].file)
        print(f'file {file}')
        data = csv.DictReader(file)
        print(f'mobile {data}')
        for i in data:
            print(i)

