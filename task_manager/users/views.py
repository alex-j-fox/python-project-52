from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from task_manager.mixins import AuthAndProfileOwnershipMixin, CustomContextMixin
from task_manager.users.forms import UserForm


class IndexView(TemplateView):
    template_name = 'users/index.html'
    extra_context = {'users': get_user_model().objects.all()}


class UserCreateView(CustomContextMixin, CreateView):
    template_name = 'users/create.html'
    form_class = UserForm
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully registered')
    model = get_user_model()
    title = _('Registration')
    action = _('Register')


class UserUpdateView(AuthAndProfileOwnershipMixin, CustomContextMixin, UpdateView):
    model = get_user_model()
    template_name = 'users/update.html'
    form_class = UserForm
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully updated')
    title = _('Change user')
    action = _('Change')


class UserDeleteView(AuthAndProfileOwnershipMixin, CustomContextMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully deleted')
