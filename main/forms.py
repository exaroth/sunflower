from django import forms
from main.models import Image


class ImageUploadForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ("title", "description", "path")
