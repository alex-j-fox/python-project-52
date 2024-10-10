from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from task_manager.mixins import AuthAndProfileOwnershipMixin, \
    SuccessMessageFormContextMixin
from task_manager.users.forms import UserForm


class IndexView(TemplateView):
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        """
        Передача контекста в шаблон с пользователями.
        """
        context = super().get_context_data(**kwargs)
        context['users'] = get_user_model().objects.all()
        return context


class UserCreateView(SuccessMessageFormContextMixin, CreateView):
    template_name = 'users/create.html'
    form_class = UserForm
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully registered')
    model = get_user_model()
    title = _('Registration')
    action = _('Register')


class UserUpdateView(AuthAndProfileOwnershipMixin,
                     SuccessMessageFormContextMixin,
                     UpdateView):
    model = get_user_model()
    template_name = 'users/update.html'
    form_class = UserForm
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully updated')
    title = _('Change user')
    action = _('Change')


class UserDeleteView(AuthAndProfileOwnershipMixin,
                     SuccessMessageFormContextMixin,
                     DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully deleted')

    def dispatch(self, request, *args, **kwargs):
        """
        Ограничение удаления пользователя, связанного с задачей.

        Перехватывает исключение ProtectedError, перенаправляет на страницу с
        пользователями и выдает сообщение об ошибке.
        """
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _('Cannot delete user because it is in use'))
            return redirect(reverse_lazy('users_index'))
