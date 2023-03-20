from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.fields import EmailField
from django.forms.forms import Form
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Student, Articles


class CreateUserForm(UserCreationForm):  # форма создания пользователя
    username = forms.CharField(label='Логин', min_length=5, max_length=150, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Е-mail')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("Пользователь уже существует")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Пользователь с таким e-mail уже зарегестрирован")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают", code='invalid')
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.clean_username(),
            self.clean_email(),
            self.clean_password2()
        )
        return user


class LoginForm(AuthenticationForm):  # форма авторизации
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        "class": "form-input u-form-group u-form-name u-label-top"
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        "class": "form-input u-form-group u-label-top"
    }))


class UserUpdateForm(forms.ModelForm):  # форма редактирования пользователя
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class StudentUpdateForm(forms.ModelForm):  # форма редактирования профиля
    class Meta:
        model = Student
        fields = ['name', 'phone', 'about', 'image']


class ArticlesUpdateForm(ModelForm):  # форма редактирования статьи
    class Meta:
        model = Articles
        fields = ['title', 'school', 'date', 'about', 'file']
        labels = {
            'title': _('Название Статьи'),
            'school': _('Учреждение'),
            'date': _('Дата публикации'),
            'about': _('Аннотация статьи'),
            'file': _('Файл со статьей'),
        }
        max_length = {
            'title': _(100),
        }
        required = {
            'school': _(False),
            'about': _(False),
        }
        widget = {
            'about': _(forms.Textarea),
        }


class ArticlesForm(ModelForm):  # форма добавления статьи
    class Meta:
        model = Articles
        fields = ['title', 'school', 'date', 'about', 'file']
        labels = {
            'title': _('Название Статьи'),
            'school': _('Учреждение'),
            'date': _('Дата публикации'),
            'about': _('Аннотация статьи'),
            'file': _('Файл со статьей'),
        }
        max_length = {
            'title': _(100),
        }
        required = {
            'school': _(False),
            'about': _(False),
        }
        widget = {
            'about': _(forms.Textarea),
        }
