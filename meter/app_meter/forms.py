from django import forms
from . import models

# TODO написать форму добавления ресурса и единиц измерения


class MeterForm(forms.ModelForm):
    class Meta:
        model = models.Meter
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                "placeholder": "Meter name",
            }),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = models.Unit
        fields = '__all__'


class ResourceForm(forms.ModelForm):
    class Meta:
        model = models.Resource
        fields = '__all__'


class ReadingsFileForm(forms.Form):
    csv_file = forms.FileField()

    def check_file_type(self):
        """Checking the file type"""
        file = self.cleaned_data['csv_file']
        if file:
            ext = file.name.split('.')[-1]
            if ext != 'csv':
                raise forms.ValidationError('File Type not supported')
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


