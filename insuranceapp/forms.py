from django import forms
from .models import agent

class LocationForm(forms.ModelForm):
    class meta:
        model = agent
        fields = ['']