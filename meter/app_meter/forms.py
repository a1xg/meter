import io
import pandas as pd
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

    def check_file_type(self):
        """Checking the file type"""
        file = self.cleaned_data['csv_file']
        print('CLEAN DATA FILE')
        if file:
            ext = file.name.split('.')[-1]
            if ext != 'csv':
                raise ValidationError('File Type not supported')
            return file

    # TODO написать сортировку, проверку формата записи, проверку наличия ошибок записи
    def process_data(self):
        file = io.TextIOWrapper(self.cleaned_data['csv_file'].file)
        date_column = ['DATE']
        df = pd.read_csv(file, sep=',', parse_dates=date_column)
        new_df = pd.DataFrame()
        new_df['absolute_value'] = df['VALUE'].astype(int)
        new_df['date'] = df['DATE']
        new_df = new_df.sort_values(by='date')
        new_df['relative_value'] = new_df['absolute_value'].diff().fillna(0)
        new_df['relative_value'] = new_df['relative_value'].astype(int)
        return new_df


