from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re

from .models import Image, UserProfile, Category
from .helpers import username_valid
from django.conf import settings


class ImageForm(forms.ModelForm):

    class Meta:

        model = Image
        fields = ("title",)


class UserProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile
        exclude = ("user",)


class UserCreateForm(forms.ModelForm):

    password2 = forms.CharField(
        widget=forms.PasswordInput({"placeholder": "Repeat password"})
    )

    def clean_username(self):

        username = self.cleaned_data.get("username", None)
        if username:
            if len(username) < 4 or len(username) > 20:
                msg = "Length of your username must be between 4 and 20 characters"
                raise forms.ValidationError(msg)
            elif not username_valid(username):
                msg = "Only letters, numbers and _ are allowed in username"
                raise forms.ValidationError(msg)
        return username

    def clean(self, *args, **kwargs):
        password1 = self.cleaned_data.get("password", None)
        password2 = self.cleaned_data.get("password2", None)
        if password1 and password2 and password1 != password2:
            msg = "Password Mismatch"
            raise forms.ValidationError(msg)
        return super(UserCreateForm, self).clean(*args, **kwargs)

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "password", "password2")
        widgets = {
            "username": forms.TextInput({"class": "my class",
                                         "placeholder": "Enter your username"}),
            "password": forms.PasswordInput({"placeholder": "Enter password"}),
        }


class ImageAddForm(forms.ModelForm):


    def clean_path(self):
        image = self.cleaned_data.get("img", None)
        if image:
            image_name = image.name
            ext = image_name.rsplit(".", 1)[-1]
            if ext and len(ext) > 1:
                if ext not in ("jpg", "png", "gif"):
                    msg = ("Supported formats are jpg and png images")
                    raise forms.ValidationError(msg)
        return image


    class Meta:
        
        model = Image
        fields = ("title", "img")

class CategoryForm(forms.ModelForm):
    

    class Meta:
        model = Category
        fields = ("name",)
        widgets = {
            "name": forms.TextInput({
                "placeholder": "Category names",
            })

    }


