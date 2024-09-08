from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.contrib import messages

from task_manager.users.forms import UserForm
from task_manager.users.models import User


class IndexView(View):
    template_name = 'users/index.html'

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request,
                      self.template_name,
                      context={'users': users})


class UserCreateView(View):
    template_name = 'users/create.html'
    title = _('Registration')
    action = _('Register')

    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request,
                      self.template_name,
                      context={'form': form,
                               'title': self.title,
                               'action': self.action})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('User successfully registered'))
            return redirect('users_index')

        return render(request,
                      self.template_name,
                      context={'form': form,
                               'title': self.title,
                               'action': self.action})


class UserUpdateView(View):
    template_name = 'users/update.html'
    title = _('Change user')
    action = _('Change')

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        form = UserForm(instance=user)
        return render(request,
                      self.template_name,
                      context={'user': user,
                               'form': form,
                               'title': self.title,
                               'action': self.action})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        print(f'Пользователь id: {user_id}')
        print(f'Пользователь: {user}')
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            print(form.data)
            messages.success(request, _('User successfully updated'))
            return redirect('users_index')
        return render(request,
                      self.template_name,
                      context={'user': user,
                               'form': form,
                               'title': self.title,
                               'action': self.action})


class UserDeleteView(View):
    template_name = 'users/delete.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        return render(request,
                      self.template_name,
                      context={'user': user})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
            messages.info(request, _('User successfully deleted'))
        return redirect('users_index')
