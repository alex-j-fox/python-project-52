from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            username='testuser',
            password='password123'
        )
        self.client = Client()
        self.client.force_login(self.user)

        self.status = Status.objects.create(name='Test status')
        self.author = self.user
        self.executor = User.objects.create_user(username='executor', password='12345')
        self.label = Label.objects.create(name='Test label')


class UnauthorizedCRUDTest(TestCase):

    def test_unauthorized_index_view(self):
        """
        Проверка доступности страницы задач без авторизации.

        Страница должна быть доступна только авторизованным пользователям.
        Неавторизованный пользователь перенаправляется на страницу входа с кодом 302.
        """
        response = self.client.get(reverse('tasks_index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_unauthorized_create(self):
        """
        Проверка доступности страницы создания задачи без авторизации.

        Страница должна быть доступна только авторизованным пользователям.
        Неавторизованный пользователь перенаправляется на страницу входа с кодом 302.
        """
        response = self.client.get(reverse('tasks_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_unauthorized_update(self):
        """
        Проверка доступности страницы изменения задачи без авторизации.

        Страница должна быть доступна только авторизованным пользователям.
        Неавторизованный пользователь перенаправляется на страницу входа с кодом 302.
        """
        response = self.client.get(reverse('tasks_update', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_unauthorized_delete(self):
        """
        Проверка доступности страницы удаления задачи без авторизации.

        Страница должна быть доступна только авторизованным пользователям.
        Неавторизованный пользователь перенаправляется на страницу входа с кодом 302
        """
        print('testing unauthorized delete')
        print('reverse tasks_delete:', reverse('tasks_delete', args=[1]))
        response = self.client.get(reverse('tasks_delete', args=[1]))
        print('response:', response)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class TasksIndexViewTest(BaseTestCase):
    def test_tasks_index_view(self):
        """
        Проверка GET-запроса на странице задач.

        Страница должна быть доступной (код 200), должен использоваться правильный
        шаблон (список задач).
        """
        response = self.client.get(reverse('tasks_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')


class TasksCreateViewTest(BaseTestCase):
    def test_tasks_create_view_get(self):
        """
        Проверка GET-запроса на странице создания задачи.

        Страница должна быть доступной (код 200), должен использоваться правильный
        шаблон (с формой создания задачи).
        """
        response = self.client.get(reverse('tasks_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')

    def test_tasks_create_view_post_valid(self):
        """
        Проверка POST-запроса на странице создания задачи с валидными данными.

        Страница должна быть перенаправлена на страницу со списком задач (код 302),
        данные должны быть сохранены в базе данных,
        количество записей в бд должно увеличиться на 1.
        """
        data = {
            'name': 'Test task',
            'description': 'Test description',
            'status': self.status.id,
            'author': self.author,
            'executor': self.executor,
            'labels': self.label.id
        }
        self.assertEqual(Task.objects.count(), 0)
        response = self.client.post(reverse('tasks_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), 1)

    def test_tasks_create_view_post_invalid(self):
        """
        Проверка POST-запроса на странице создания задачи с невалидными данными.

        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        создания задачи, количество записей в бд не должно измениться.
        """
        data = {
            'name': '',
            'description': 'Test description',
            'status': 1,
            'executor': 1,
            'labels': 1
        }
        self.assertEqual(Task.objects.count(), 0)
        response = self.client.post(reverse('tasks_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')
        self.assertEqual(Task.objects.count(), 0)

    def test_tasks_create_view_post_unique(self):
        """
        Проверка POST-запроса на странице создания задачи с уникальной задачей.

        После попытки создать задачу с уже существующим именем, страница должна быть
        доступной (код 200), должен использоваться шаблон с формой создания задачи,
        неуникальные данные не должны быть сохранены в базе данных,
        количество записей в бд не должно измениться.
        """
        data1 = {
            'name': 'Test task',
            'description': 'Test description',
            'status': self.status.id,
            'author': self.author,
            'executor': self.executor,
            'labels': self.label.id
        }
        data2 = {
            'name': 'Test task',
            'description': 'Test description new',
            'status': self.status.id,
            'author': self.author,
            'executor': '',
            'labels': ''
        }
        self.assertEqual(Task.objects.count(), 0)
        self.client.post(reverse('tasks_create'), data1)
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(reverse('tasks_create'), data2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')
        self.assertEqual(Task.objects.count(), 1)


class TasksUpdateViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.post(reverse('tasks_create'), {
            'name': 'Test task',
            'description': 'Test description',
            'status': self.status.id,
            'author': self.author,
            'executor': self.executor,
            'labels': self.label.id
        })
        self.task = Task.objects.first()

    def test_tasks_update_view_get(self):
        """
        Проверка GET-запроса на странице редактирования задачи.

        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        редактирования задачи.
        """
        response = self.client.get(reverse('tasks_update', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')

    def test_tasks_update_view_post_valid(self):
        """
        Проверка POST-запроса на странице редактирования задачи с валидными данными.

        Изменяем имя и описание задачи. Страница должна быть перенаправлена на страницу
        со списком задач (код 302), данные должны быть сохранены в базе данных.
        Количество записей в бд не должно измениться.
        Имя и описание задачи в базе данных должно соответствовать введенным значениям.
        """
        data = {
            'name': 'Test task updated',
            'description': 'Test description updated',
            'status': Status.objects.create(name='New test status').id,
            'author': self.author,
            'executor': self.executor,
            'labels': self.label.id
        }
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(
            reverse('tasks_update', kwargs={'pk': self.task.pk}), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), 1)
        updated_task = Task.objects.first()
        self.assertEqual(updated_task.name, 'Test task updated')
        self.assertEqual(updated_task.description, 'Test description updated')

    def test_tasks_update_view_post_invalid(self):
        """
        Проверка POST-запроса на странице редактирования задачи с невалидными данными.

        При попытке изменить данные на невалидные значения страница должна быть
        доступна (код 200), должен использоваться шаблон с формой редактирования задачи,
        количество записей в базе данных не должно изменяться.
        Должно появляться сообщение об ошибке.
        Данные записи в базе данных не должны измениться.
        """
        data = {
            'name': '',
            'description': '',
            'status': '',
            'author': self.author,
            'executor': 1,
            'labels': 1
        }
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(
            reverse('tasks_update', kwargs={'pk': self.task.pk}), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.name, 'Test task')

    def test_tasks_update_view_post_unique(self):
        """
        Проверка POST-запроса на странице редактирования задачи с невалидными данными.

        Создаем вторую задачу. Пытаемся изменить имя на имя первой задачи.
        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        редактирования задачи, количество записей в базе данных не должно изменяться.
        Должно появляться сообщение об ошибке.
        Имя задачи не должно измениться.
        """
        new_status = Status.objects.create(name='New test status')
        data_second = {
            'name': 'Test task new',
            'description': 'Test description new',
            'status': new_status.id,
            'author': self.author,
            'executor': User.objects.create_user(username='new_worker',
                                                 password='12345'),
            'labels': self.label.id
        }
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(reverse('tasks_create'), data_second)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), 2)

        data_first = {
            'name': 'Test task new',
            'description': 'Test description new',
            'status': self.status.id,
            'author': self.author,
            'executor': self.executor,
            'labels': ''
        }
        response = self.client.post(
            reverse('tasks_update', kwargs={'pk': self.task.pk}), data_first)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(self.task.name, 'Test task')


class TaskDeleteViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.post(reverse('tasks_create'), {
            'name': 'Test task',
            'description': 'Test description',
            'status': self.status.id,
            'author': self.author,
            'executor': self.executor,
            'labels': self.label.id
        })
        self.task = Task.objects.first()

    def test_tasks_delete_view_get(self):
        """
        Проверка GET-запроса на странице удаления задачи.

        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        удаления задачи.
        """
        response = self.client.get(
            reverse('tasks_delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete.html')

    def test_tasks_delete_view_post(self):
        """
        Проверка POST-запроса на странице удаления задачи.

        Количество записей в базе данных - 1. После удаления задачи страница должна быть
        перенаправлена на страницу со списком задач (код 302),
        количество записей в базе данных должно уменьшиться на 1.
        """
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(
            reverse('tasks_delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), 0)


class TaskDetailViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.post(reverse('tasks_create'), {
            'name': 'Test task',
            'description': 'Test description',
            'status': self.status.id,
            'author': self.author,
            'executor': self.executor,
            'labels': self.label.id
        })
        self.task = Task.objects.first()

        self.task_form = TaskForm(instance=self.task)

    def test_tasks_detail_view_get(self):
        """
        Проверка GET-запроса на странице просмотра задачи.

        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        просмотра задачи.
        """
        response = self.client.get(
            reverse('tasks_detail', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/detail.html')
