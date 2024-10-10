from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, \
    DetailView

from task_manager.mixins import SuccessMessageFormContextMixin, CustomLoginRequiredMixin
from task_manager.tasks.forms import TaskForm, TaskFilterForm
from task_manager.tasks.models import Task


class IndexView(CustomLoginRequiredMixin, TemplateView):
    template_name = 'tasks/index.html'
    form_class = TaskFilterForm
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        """
        Обработка формы фильтра.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            tasks = Task.objects.all()
            if form.cleaned_data.get('status'):
                tasks = tasks.filter(status=form.cleaned_data.get('status'))
            if form.cleaned_data.get('executor'):
                tasks = tasks.filter(executor=form.cleaned_data.get('executor'))
            if form.cleaned_data.get('label'):
                tasks = tasks.filter(labels=form.cleaned_data.get('label'))
            if form.cleaned_data.get('self_tasks'):
                tasks = tasks.filter(author=request.user)
            return render(request,
                          self.template_name,
                          context={'tasks': tasks,
                                   'form': form})
        else:
            return render(request,
                          self.template_name,
                          context={'tasks': Task.objects.all(),
                                   'form': form})


class TaskCreateView(CustomLoginRequiredMixin,
                     SuccessMessageFormContextMixin,
                     CreateView):
    template_name = 'tasks/create.html'
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully created')
    title = _('Create task')
    action = _('Create')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        """
        Обработка формы после ее валидации.

        Устанавливает текущего пользователя в качестве автора задачи.
        """
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response


class TaskDetailView(CustomLoginRequiredMixin,
                     SuccessMessageFormContextMixin,
                     DetailView):
    template_name = 'tasks/detail.html'
    model = Task
    pk_url_kwarg = 'pk'
    context_object_name = 'task'
    form_class = TaskForm
    title = _('View a task')
    login_url = reverse_lazy('login')


class TaskUpdateView(CustomLoginRequiredMixin,
                     SuccessMessageFormContextMixin,
                     UpdateView):
    template_name = 'tasks/update.html'
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully updated')
    title = _('Change task')
    action = _('Change')
    login_url = reverse_lazy('login')

    def get_redirect_url(self):
        return self.login_url


class TaskDeleteView(CustomLoginRequiredMixin,
                     SuccessMessageFormContextMixin,
                     DeleteView):
    template_name = 'tasks/delete.html'
    model = Task
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully deleted')
    title = _('Deleting a task')
    login_url = reverse_lazy('login')

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
