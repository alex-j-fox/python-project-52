from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        """
        Инициализация формы.

        Передаем в конструктор базовой формы обязательные поля.
        """
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        )

    def clean_username(self):
        """
        Функция проверяет, существует ли пользователь с таким именем.

        Если пользователь с таким именем существует, выбрасывается исключение
        ValidationError с описанием ошибки.
        """
        username = self.cleaned_data['username']
        error_message = _('A user with that username already exists.')
        if get_user_model().objects.filter(username=username).exclude(
                id=self.instance.id).exists():
            raise forms.ValidationError(error_message)
        return username
