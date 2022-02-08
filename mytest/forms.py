"Forms for mytest"
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UploadScanSetFileForm(forms.Form):
    picture = forms.FileField()
    fringe = forms.FileField()
    nolight = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Send'))
        self.helper.add_input(Submit('cancel', 'Fortryd', css_class='btn-secondary', formnovalidate='formnovalidate', formaction='/'))
