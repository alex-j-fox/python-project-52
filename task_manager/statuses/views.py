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


class IndexView(CustomIndexView):
    template_name = 'statuses/index.html'
    model = Status
    context_object_name = 'statuses'


class StatusCreateView(CustomCreateView):
    template_name = 'statuses/create.html'
    form_class = StatusForm
    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully created')


class StatusUpdateView(CustomUpdateView):
    template_name = 'statuses/update.html'
    form_class = StatusForm
    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully updated')


class StatusDeleteView(CustomDeleteView):
    template_name = 'statuses/delete.html'
    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully deleted')
    error_message = _('Cannot delete status because it is in use')

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
