from .models import Cryptdb
from django import forms

class InputForm(forms.ModelForm):
    class Meta:
        model = Cryptdb
        fields = ('function', 'type', 'inputfile')

        widgets = {
            'function': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'inputfile': forms.FileInput(attrs={'class': 'form-control'})
        }