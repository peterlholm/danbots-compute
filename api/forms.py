"""
forms for testing api
"""

import os
from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

def validate_file_extension(value):
    "validate if extension is picture"
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg',]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only jpg allowed.')

class Form3dScan(forms.Form):
    "form for 3d scan set"
    deviceid = forms.CharField(required=True, max_length=32, strip=True)
    pictureno = forms.IntegerField(required=True)
    color_picture = forms.ImageField(label="Color Picture", required=True, validators=[validate_file_extension])
    dias_picture = forms.ImageField(label="Dias Picture", required=True, validators=[validate_file_extension])
    noLight_picture = forms.ImageField(label="NoLight Picture", required=True, validators=[validate_file_extension])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Send'))
        self.helper.add_input(Submit('cancel', 'Fortryd', css_class='btn-secondary', formnovalidate='formnovalidate', formaction='/'))

# class SaveFileForm(forms.Form):
#     file = forms.FileField()
#     def __init__(self, *args, **kwargs):
#         #super(SaveFileForm, self).__init__(*args, **kwargs)
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_tag = True
#         self.helper.add_input(Submit('submit', 'Send'))
#         self.helper.add_input(Submit('cancel', 'Fortryd', css_class='btn-secondary', formnovalidate='formnovalidate', formaction='/'))
