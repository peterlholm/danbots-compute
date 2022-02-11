"Forms for mytest"
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UploadScanSetFileForm(forms.Form):
    color = forms.FileField(label="Color Picture")
    fringe = forms.FileField(label="Fringe Picture")
    nolight = forms.FileField(label="Nolight Picture")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Send'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-secondary', formnovalidate='formnovalidate', formaction='/'))
