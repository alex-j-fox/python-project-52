from task_manager.tasks.models import Task


def filter_by_self_tasks(filters, request):
    """
    Фильтр задач по ключу self_tasks в фильтрах.

    Если в фильтрах существует ключ self_tasks, функция вернет QuerySet задач,
    автором которых является текущий пользователь, в противном случае будут возвращены
    все задачи.
    """
    if filters.get('self_tasks'):
        return Task.objects.filter(author=request.user)
    return Task.objects.all()


def filter_by_other_fields(tasks, filters):
    """
    Фильтр задач по другим ключам в фильтрах.

    Возвращает QuerySet задач, удовлетворяющих фильтрующимся параметрам.
    """
    other_filters = {k: v for k, v in filters.items() if v and k != 'self_tasks'}
    return tasks.filter(**other_filters)


def filter_tasks(form, request):
    """
    Фильтрует задачи на основе данных, предоставленных в форме.

    В форме предусмотрен набор фильтров, которые используются для фильтрации задач.
    Фильтры можно комбинировать любым способом, чтобы сузить список задач.
    """
    filters = form.cleaned_data
    tasks = filter_by_self_tasks(filters, request)
    tasks = filter_by_other_fields(tasks, filters)
    return tasks
