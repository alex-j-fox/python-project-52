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
    protected_error_message = _('Cannot delete label because it is in use')
    redirect_url = reverse_lazy('labels_index')
