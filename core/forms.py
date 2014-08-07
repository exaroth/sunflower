from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Image, UserProfile





class ImageForm(forms.ModelForm):

    class Meta:

        model = Image
        fields = ("title",)


class UserProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile
        exclude = ("user",)


class UserCreateForm(forms.ModelForm):

    password2 = forms.CharField(widget=forms.PasswordInput)

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
            "password2": forms.PasswordInput({"placeholder": "Repeat password"}),
        }
