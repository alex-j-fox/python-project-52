from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from task_manager.users.forms import LoginForm


def index(request):
    return render(request, 'index.html')


class LoginUserView(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'
    success_url = 'index'

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, _('You are logged in'))
        return redirect(self.success_url)


class LogoutUserView(LogoutView):

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _('You are logged out'))
        return redirect('login')


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)
