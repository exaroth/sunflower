from django import forms
from django.contrib.auth.models import User

from .models import Image





class ImageForm(forms.ModelForm):

    class Meta:

        model = Image
        fields = ("title",)



class UserCreateForm(forms.ModelForm):

    class Meta:

        model = User
        fields = ("username", "password")
        widgets = {
            "username": forms.TextInput({"class": "my class",
                                         "placeholder": "Enter your username"}),
            "password": forms.PasswordInput({"placeholder": "Enter password"})
        }
