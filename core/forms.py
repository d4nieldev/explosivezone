from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'שם פרטי', 'style': 'direction:rtl'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'שם משפחה', 'style': 'direction:rtl'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'אימייל', 'autocomplete': 'new-password'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'שם משתמש', 'autocomplete': 'new-password'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'סיסמא', 'autocomplete': 'new-password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'אימות סיסמא', 'autocomplete': 'new-password'}))

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2' )
