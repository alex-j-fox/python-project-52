from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    username = models.CharField(
        max_length=50,
        verbose_name=_("Username"),
        unique=True,
        help_text=_("Required field. No more than 150 characters. Only letters, numbers and symbols @/./+/-/_.") # noqa
    )
    password1 = models.CharField(
        max_length=50,
        verbose_name=_("Password"),
        help_text=_("Your password must contain at least 3 characters.")
    )
    password2 = models.CharField(
        max_length=50,
        verbose_name=_("Password confirmation"),
        help_text=_("To confirm, please enter your password again.")
    )
    first_name = models.CharField(max_length=50, verbose_name=_("First name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last name"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def set_password(self, password):
        self.password1 = password
        self.password2 = password
