from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'status',
            'executor',
            'labels',
        )
        required_fields = ('name', 'description', 'status')


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(label=_('Status'), queryset=Status.objects.all(),
                                    required=False)
    executor = forms.ModelChoiceField(label=_('Executor'), queryset=User.objects.all(),
                                      required=False)
    labels = forms.ModelChoiceField(label=_('Label'), queryset=Task.objects.all(),
                                    required=False)
    self_tasks = forms.BooleanField(label=_('Only your tasks'), required=False)
