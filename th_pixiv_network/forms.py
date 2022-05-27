from django import forms
from .widgets import RangeInput
from django.core.validators import MaxValueValidator, MinValueValidator

class NumberForm(forms.Form):
    threshold = forms.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])