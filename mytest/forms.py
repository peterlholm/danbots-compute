"Forms for mytest"
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from compute.settings import DEVICE_PATH

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

class DeviceForm(forms.Form):
    def gen_device_list():
        flist = []
        for folder in DEVICE_PATH.glob('*'):
            #print(folder)
            flist.append((folder.name,folder.name))
        return flist

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-offset-2 col-lg-3'
        self.helper.field_class = 'col-lg-7'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.add_input(Submit('submit', 'show'))
        self.helper.add_input(Submit('submit', 'GetFolderSet'))
        self.helper.add_input(Submit('cancel', 'Fortryd', css_class='btn-secondary', formnovalidate='formnovalidate', formaction='/models/trainlist'))

    device = forms.ChoiceField(choices=gen_device_list())
    