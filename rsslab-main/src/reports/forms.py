from django import forms

from .models import CsvUpload


class CsvUploadForm(forms.ModelForm):
    class Meta:
        model = CsvUpload
        fields = '__all__'
