from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.mixins import (CustomIndexView,
                                 CustomCreateView,
                                 CustomUpdateView,
                                 CustomDeleteView)


class IndexView(CustomIndexView):
    template_name = 'labels/index.html'
    model = Label
    context_object_name = 'labels'


class LabelCreateView(CustomCreateView):
    template_name = 'labels/create.html'
    form_class = LabelForm
    model = Label
    success_url = reverse_lazy('labels_index')
    success_message = _('Label successfully created')


class LabelUpdateView(CustomUpdateView):
    template_name = 'labels/update.html'
    form_class = LabelForm
    model = Label
    success_url = reverse_lazy('labels_index')
    success_message = _('Label successfully updated')


class LabelDeleteView(CustomDeleteView):
    template_name = 'labels/delete.html'
    model = Label
    success_url = reverse_lazy('labels_index')
    success_message = _('Label successfully deleted')
    error_message = _('Cannot delete label because it is in use')

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
