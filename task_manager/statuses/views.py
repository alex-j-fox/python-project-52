from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import (CustomIndexView,
                                 CustomCreateView,
                                 CustomUpdateView,
                                 CustomDeleteView)
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


# class IndexView(CustomLoginRequiredMixin, TemplateView):
class IndexView(CustomIndexView):
    template_name = 'statuses/index.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        """
        Передача контекста в шаблон.
        """
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        return context


class StatusCreateView(CustomCreateView):
    template_name = 'statuses/create.html'
    form_class = StatusForm
    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully created')
    title = _('Create status')
    action = _('Create')
    login_url = reverse_lazy('login')


class StatusUpdateView(CustomUpdateView):
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


class StatusDeleteView(CustomDeleteView):
    template_name = 'statuses/delete.html'
    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully deleted')
    error_message = _('Cannot delete status because it is in use')
    title = _('Deleting a status')
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        """
        Обработка формы удаления.

        При успешном удалении статуса показываем сообщение об успешном удалении и
        перенаправляем пользователя на страницу со списком статусов.
        Если статус защищен от удаления, показываем сообщение об ошибке и перенаправляем
        пользователя на страницу со списком статусов.
        """
        try:
            response = super().delete(request, *args, **kwargs)
            if response.status_code == 302:
                messages.success(request, self.success_message)
            return response
        except ProtectedError:
            messages.error(request, self.error_message)
            return redirect(self.success_url)
