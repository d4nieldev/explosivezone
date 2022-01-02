import django.db.utils
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from core.models import MenuOption, Exercise

import logging


class UserForm(UserCreationForm):
    """
    User registration form. consists of:
    first name, last name, email, username, password, password confirmation.
    all text input field.
    """
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'שם פרטי', 'style': 'direction:rtl'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'שם משפחה', 'style': 'direction:rtl'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'אימייל', 'autocomplete': 'new-password'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'שם משתמש', 'autocomplete': 'new-password'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'סיסמא', 'autocomplete': 'new-password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'אימות סיסמא', 'autocomplete': 'new-password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class MenuOptionForm(forms.ModelForm):
    """
    Add menu option form. consists of:
    select field to select which category will be the parent of the new one.
    text input field for the title of the new category.
    """
    try:
        class Meta:
            model = MenuOption
            fields = ('parent', 'title')
            widgets = {
                'parent': forms.Select(
                    attrs={'class': 'form-control mb-1'}, choices=[(m, m) for m in MenuOption.objects.all()]),
                'title': forms.TextInput(
                    attrs={'class': 'form-control', 'placeholder': 'כותרת'})
            }
    except django.db.utils.ProgrammingError:
        # if the migration is not built yet the error will be raised
        # so we can ignore this part for the migration process to work
        logging.debug("Skipped MenuOptionForm because MenuOption model does not exist!")


class ExerciseForm(forms.ModelForm):
    """
    Add exercise form. consists of:
    a textarea for the description of the exercise.
    text input for the video code from youtube.
    (https://www.youtube.com/watch?v=<video_code>)
    """
    class Meta:
        model = Exercise
        fields = ('description', 'video_code',)
        widgets = {
            'description': forms.Textarea(),
            'video_code': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 15rem;'})
        }
