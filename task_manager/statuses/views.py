from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from task_manager.mixins import CustomContextMixin, CustomLoginRequiredMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class IndexView(LoginRequiredMixin, View):
    template_name = 'statuses/index.html'

    def get(self, request, *args, **kwargs):
        """
        Вывод списка статусов.
        """
        statuses = Status.objects.all()
        return render(request,
                      self.template_name,
                      context={'statuses': statuses})


class StatusCreateView(CustomLoginRequiredMixin, CustomContextMixin, CreateView):
    template_name = 'statuses/create.html'
    form_class = StatusForm
    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully created')
    title = _('Create status')
    action = _('Create')
    login_url = reverse_lazy('login')


class StatusUpdateView(CustomLoginRequiredMixin, CustomContextMixin, UpdateView):
    template_name = 'statuses/update.html'
    form_class = StatusForm
    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully updated')
    title = _('Change status')
    action = _('Change')
    login_url = reverse_lazy('login')

    def get_redirect_url(self):
        return self.login_url


class StatusDeleteView(CustomLoginRequiredMixin, CustomContextMixin, DeleteView):
    template_name = 'statuses/delete.html'
    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully deleted')
    title = _('Deleting a status')
    login_url = reverse_lazy('login')
