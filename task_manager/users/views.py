from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, FormView

from task_manager.users.forms import UserForm
from task_manager.users.mixins import AuthAndProfileOwnershipMixin


class IndexView(View):
    template_name = 'users/index.html'

    def get(self, request, *args, **kwargs):
        """
        Вывод списка пользователей.
        """
        users = get_user_model().objects.all()
        return render(request,
                      self.template_name,
                      context={'users': users})


class ContextMixin(SuccessMessageMixin, FormView):
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


class UserCreateView(ContextMixin, CreateView):
    template_name = 'users/create.html'
    form_class = UserForm
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully registered')
    model = get_user_model()
    title = _('Registration')
    action = _('Register')


class UserUpdateView(AuthAndProfileOwnershipMixin, ContextMixin, UpdateView):
    model = get_user_model()
    template_name = 'users/update.html'
    form_class = UserForm
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully updated')
    title = _('Change user')
    action = _('Change')


class UserDeleteView(SuccessMessageMixin, AuthAndProfileOwnershipMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully deleted')
