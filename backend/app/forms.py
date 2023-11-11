from django import forms

class CityForm(forms.Form):
    city = forms.CharField(label='Enter a city', max_length=100)