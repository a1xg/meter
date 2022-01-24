from django import forms
from . import models


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
        fields = ['name']


class ResourceForm(forms.ModelForm):
    class Meta:
        model = models.Resource
        fields = ['name']


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
