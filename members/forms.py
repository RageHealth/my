
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from PIL import Image

from .models import Profile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
    

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    email = forms.EmailField(label="Email", max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'name': 'email'}))
    password1 = forms.CharField(label="Password", max_length=30,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password1'}))
    password2 = forms.CharField(label="Password confirmation", max_length=30,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password2'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'date_of_birth', 'bio', 'tiktokurl', 'youtubeurl', 'shapka']
        labels = {
            'avatar': 'Выберите аватар',
            'date_of_birth': 'Дата рождения',
            'bio': 'О себе',
            'tiktokurl': 'URL TikTok',
            'youtubeurl': 'URL YouTube',
            'shapka': 'Добавьте фотографию с розширением  2048 × 1152',
            # Add labels for other fields as needed
        }
        widgets = {
            'shapka': forms.FileInput(attrs={'class': 'form-control-file'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tiktokurl': forms.URLInput(attrs={'class': 'form-control'}),
            'youtubeurl': forms.URLInput(attrs={'class': 'form-control'})
            # Add more fields with Bootstrap styles as needed
        }

    def clean_shapka(self):
        shapka = self.cleaned_data.get('shapka', False)
        if shapka:
            if shapka.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Фото шапки не должно быть больше 10 МБ")
        return shapka

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        if dob > datetime.date.today():
            raise ValidationError(_("Date of birth cannot be in the future"))
        return dob