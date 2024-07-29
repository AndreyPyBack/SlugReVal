from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django import forms
from .models import Product


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", 'captcha']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'slug']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Цена должна быть положительной.')
        return price


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
