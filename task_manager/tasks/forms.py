import django_filters
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
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


class TaskFilterForm(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(label=_('Label'),
                                              queryset=Label.objects.all())
    self_tasks = django_filters.BooleanFilter(label=_('Only your tasks'),
                                              widget=forms.CheckboxInput,
                                              method='filter_by_self_tasks',
                                              required=False)

    def filter_by_self_tasks(self, queryset, author, value):
        """
        Фильтрация задач по текущему пользователю.
        """
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor']
