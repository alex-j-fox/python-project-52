from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import (CustomIndexView,
                                 CustomCreateView,
                                 CustomUpdateView,
                                 CustomDetailView,
                                 CustomDeleteView)
from task_manager.tasks.forms import TaskForm, TaskFilterForm
from task_manager.tasks.models import Task
from task_manager.tasks.utils import filter_tasks


class IndexView(CustomIndexView):
    template_name = 'tasks/index.html'
    form_class = TaskFilterForm

    def get_context_data(self, **kwargs):
        """
        Передача контекста в шаблон с задачами и формой фильтрации.
        """
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        """
        Обработка формы фильтра.

        Если применяются фильтры, функция возвращает отфильтрованные задачи.
        Иначе функция возвращает все задачи.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            tasks = filter_tasks(form, request)
            return render(request,
                          self.template_name,
                          context={'tasks': tasks,
                                   'form': form})
        else:
            return render(request,
                          self.template_name,
                          context={'tasks': Task.objects.all(),
                                   'form': form})


class TaskCreateView(CustomCreateView):
    template_name = 'tasks/create.html'
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully created')
    title = _('Create task')

    def form_valid(self, form):
        """
        Обработка формы после ее валидации.

        Устанавливает текущего пользователя в качестве автора задачи.
        """
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response


class TaskDetailView(CustomDetailView):
    template_name = 'tasks/detail.html'
    model = Task
    pk_url_kwarg = 'pk'
    context_object_name = 'task'
    form_class = TaskForm
    title = _('View a task')


class TaskUpdateView(CustomUpdateView):
    template_name = 'tasks/update.html'
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully updated')
    title = _('Change task')


class TaskDeleteView(CustomDeleteView):
    template_name = 'tasks/delete.html'
    model = Task
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully deleted')
    title = _('Deleting a task')

    def dispatch(self, request, *args, **kwargs):
        """
        Проверка прав на удаление задачи.

        Неавторизованный пользователь перенаправляется на страницу входа.
        Авторизованный пользователь не может удалять задачу, если не является её автором
        """
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, _('Only the author can delete the task'))
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
