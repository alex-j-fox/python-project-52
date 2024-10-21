from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.mixins import AuthAndProfileOwnershipMixin
from task_manager.users.forms import UserForm
from task_manager.users.models import User


class IndexView(ListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/create.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')


class UserUpdateView(AuthAndProfileOwnershipMixin,
                     SuccessMessageMixin,
                     UpdateView):
    template_name = 'users/update.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully updated')


class UserDeleteView(AuthAndProfileOwnershipMixin,
                     SuccessMessageMixin,
                     DeleteView):
    template_name = 'users/delete.html'
    model = User
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully deleted')

    def form_valid(self, form):
        """
        Проверяет возможность удаления пользователя.

        Если пользователь связан с задачей, его невозможно удалить.
        В этом случае пользователь перенаправляется на страницу со списком
        пользователей с сообщением об ошибке.
        """
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request,
                           _('Cannot delete user because it is in use'))
            return redirect(self.success_url)
