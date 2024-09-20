from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class AuthAndProfileOwnershipMixin(UserPassesTestMixin):

    def handle_no_permission(self):
        """
        Обработка ошибки при попытке изменения чужого профиля.

        Если пользователь не авторизован, выдаем сообщение об ошибке и перенаправляем на
        страницу входа.
        Если пользователь авторизован, выдаем сообщение об ошибке и перенаправляем на
        страницу с пользователями.
        """
        if not self.request.user.is_authenticated:
            messages.error(self.request, _("You are not authorized! Please log in."))
            return redirect('login')
        messages.error(self.request,
                       _("You don't have permission to change other user"))
        return redirect('users_index')

    def test_func(self):
        """
        Проверка, является ли текущий пользователь владельцем профиля.
        """
        user_id = self.kwargs.get('pk')
        return self.request.user.pk == user_id
