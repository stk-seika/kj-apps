from django import forms
from django.forms import ValidationError

def size_limit_validator(value):
    file_size= value.size
    if file_size > 52428800:    # 50MB = 52428800
        raise ValidationError('File size over')

class ImageForm(forms.Form):
    image = forms.ImageField(validators=[size_limit_validator])
    # template_name = "classifier/classifier.html"