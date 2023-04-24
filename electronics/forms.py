from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Order


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    captcha = CaptchaField()
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Repeat Password"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "captcha"]


# class AddCartForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['user', 'product']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
