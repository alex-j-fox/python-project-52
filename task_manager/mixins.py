from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView


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


class SuccessMessageFormContextMixin(SuccessMessageMixin, FormView):
    title = ''
    action = ''

    def get_context_data(self, **kwargs):
        """
        Передача данных (название формы, текст кнопки) в контекст
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['action'] = self.action
        return context


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        """
        Обработка ошибок для неавторизованного пользователя.

        Если пользователь не авторизован, перенаправляем на страницу входа.
        """
        return redirect(self.login_url)
