from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  DetailView)

LOGIN_URL = reverse_lazy('login')


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


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = LOGIN_URL

    def handle_no_permission(self):
        """
        Обработка ошибок для неавторизованного пользователя.

        Если пользователь не авторизован, перенаправляем на страницу входа.
        """
        return redirect(self.login_url)


class ProtectedErrorHandlerMixin:
    protected_error_message = None
    redirect_url = None

    def post(self, request, *args, **kwargs):
        """
        Обработка ошибок для защищенных ресурсов.
        """
        try:
            return super().post(request, *args, **kwargs)  # noqa
        except ProtectedError:
            messages.error(request, self.protected_error_message)
            return redirect(self.redirect_url)


class CustomIndexView(CustomLoginRequiredMixin,
                      ListView):
    pass


class CustomCreateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       CreateView):
    pass


class CustomUpdateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       UpdateView):
    def get_redirect_url(self):
        return self.login_url


class CustomDeleteView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       DeleteView):
    pass


class CustomDetailView(ProtectedErrorHandlerMixin,
                       CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       DetailView):
    pass
