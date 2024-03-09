from django import forms


class ImageCutterForm(forms.Form):
    file_type = forms.CharField(max_length=32, required=True)
    file_source = forms.FileField( max_length=64, required=True)
