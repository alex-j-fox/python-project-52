from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User


class UserForm(UserCreationForm):
    username = forms.CharField(
        max_length=50,
        label=_("Username"),
        help_text=_("Required field. No more than 150 characters. Only letters, numbers and symbols @/./+/-/_.") # noqa
    )
    password1 = forms.CharField(
        max_length=50,
        label=_("Password"),
        widget=forms.PasswordInput(attrs={type: 'password'}),
        help_text=_("Your password must contain at least 3 characters.")
    )
    password2 = forms.CharField(
        max_length=50,
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={type: 'password'}),
        help_text=_("To confirm, please enter your password again.")
    )
    first_name = forms.CharField(max_length=50, label=_("First name"), required=True)
    last_name = forms.CharField(max_length=50, label=_("Last name"), required=True)

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'type': 'text',
            'name': 'username',
            'autofocus': '',
            'autocapitalize': 'none',
            'autocomplete': 'username',
            'class': 'form-control',
            'placeholder': _('Username'),
            'required': '',
            'id': 'id_username',
        }),
        error_messages={
            'required': _('Please enter your username.'),
            'invalid': _('Please enter a valid username.')
        })
    password = forms.CharField(
        max_length=50,
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'name': 'password',
            'autocomplete': 'current-password',
            'class': 'form-control',
            'placeholder': _('Password'),
            'required': '',
            'id': 'id_password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'password')
