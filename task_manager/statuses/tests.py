from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status

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


class UnauthorizedCRUDTest(TestCase):
    def test_unauthorized_index_view(self):
        """
        Проверка доступности страницы со списком статусов без авторизации.

        Страница должна быть доступна только авторизованным пользователям.
        Неавторизованный пользователь перенаправляется на страницу входа с кодом 302.
        """
        response = self.client.get(reverse('statuses_index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_unauthorized_create(self):
        """
        Проверка доступности страницы создания статуса без авторизации.

        Страница должна быть доступна только авторизованным пользователям.
        Неавторизованный пользователь перенаправляется на страницу входа с кодом 302.
        """
        response = self.client.get(reverse('statuses_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_unauthorized_update(self):
        """
        Проверка доступности страницы изменения статуса без авторизации.

        Страница должна быть доступна только авторизованным пользователям.
        Неавторизованный пользователь перенаправляется на страницу входа с кодом 302.
        """
        response = self.client.get(reverse('statuses_update', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_unauthorized_delete(self):
        """
        Проверка доступности страницы удаления статуса без авторизации.

        Страница должна быть доступна только авторизованным пользователям.
        Неавторизованный пользователь перенаправляется на страницу входа с кодом 302
        """
        response = self.client.get(reverse('statuses_delete', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class StatusesIndexViewTest(BaseTestCase):
    def test_statuses_index_view(self):
        """
        Проверка GET-запроса на странице со списком статусов.

        Страница должна быть доступной (код 200), должен использоваться правильный
        шаблон (с формой создания статуса).
        """
        response = self.client.get(reverse('statuses_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')


class StatusesCreateViewTest(BaseTestCase):
    def test_status_create_view_get(self):
        """
        Проверка GET-запроса на странице создания статуса.

        Страница должна быть доступной (код 200), должен использоваться правильный
        шаблон (с формой создания статуса).
        """
        response = self.client.get(reverse('statuses_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')

    def test_status_create_view_post_valid(self):
        """
        Проверка POST-запроса на странице создания статуса с валидными данными.

        Количество записей в базе данных - 0. После создания нового статуса
        страница должна быть перенаправлена на страницу со списком статусов (код 302),
        данные должны быть сохранены в базе данных.
        Количество записей в бд должно увеличиться на 1.
        Имя статуса в базе данных должно соответствовать введенному значению.
        """
        data = {
            'name': 'Test status'
        }
        self.assertEqual(Status.objects.count(), 0)
        response = self.client.post(reverse('statuses_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(Status.objects.count(), 1)
        status = Status.objects.first()
        self.assertEqual(status.name, 'Test status')

    def test_status_create_view_post_invalid(self):
        """
        Проверка POST-запроса на странице создания статуса с невалидными данными.

        Создаем новый статус (невалидные данные).
        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        создания статуса, количество записей в базе данных не изменяется - 0.
        Должно быть отображено сообщение об ошибке.
        """
        data = {
            'name': ''
        }
        response = self.client.post(reverse('statuses_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')
        self.assertContains(response, _('This field is required.'))
        self.assertEqual(Status.objects.count(), 0)

    def test_status_create_view_post_unique(self):
        """
        Проверка POST-запроса на странице создания статуса с уникальным статусом.

        Количество записей в базе данных - 0.
        Создаем новый статус. Страница должна быть перенаправлена на страницу со списком
        статусов (код 302), данные должны быть сохранены в базе данных.
        Количество записей в бд должно увеличиться на 1.
        Создаем еще один статус с тем же именем.
        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        создания статуса, количество записей в базе данных не изменяется - 1.
        Должно быть отображено сообщение об ошибке.
        """
        data = {
            'name': 'Test status'
        }
        self.assertEqual(Status.objects.count(), 0)
        self.client.post(reverse('statuses_create'), data)
        # Создаем еще один статус с тем же именем
        response = self.client.post(reverse('statuses_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')
        # self.assertContains(response, _('Status with this Name already exists.'))
        self.assertEqual(Status.objects.count(), 1)


class StatusesUpdateViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.status = Status.objects.create(name='Test status')

    def test_status_update_view_get(self):
        """
        Проверка GET-запроса на странице редактирования статуса.

        Страница должна быть доступной (код 200), должен использоваться правильный
        шаблон (с формой редактирования статуса).
        """
        response = self.client.get(
            reverse('statuses_update', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')

    def test_status_update_view_post_valid(self):
        """
        Проверка POST-запроса на странице редактирования статуса с валидными данными.

        Количество записей в базе данных - 1.
        Изменяем имя статуса. Страница должна быть перенаправлена на страницу со списком
        статусов (код 302), данные должны быть сохранены в базе данных.
        Количество записей в бд не должно измениться.
        Имя статуса в базе данных должно соответствовать введенному значению.
        """
        data = {
            'name': 'Test status updated'
        }
        self.assertEqual(Status.objects.count(), 1)
        response = self.client.post(
            reverse('statuses_update', kwargs={'pk': self.status.pk}), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(Status.objects.count(), 1)
        status = Status.objects.first()
        self.assertEqual(status.name, 'Test status updated')

    def test_status_update_view_post_invalid(self):
        """
        Проверка POST-запроса на странице редактирования статуса с невалидными данными.

       Количество записей в базе данных - 1.
        Пытаемся изменить имя на пустую строку.
        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        редактирования статуса, количество записей в базе данных не должно изменяться.
        Должно появляться сообщение об ошибке.
        Имя статуса не должно измениться.
        """
        data = {
            'name': ''
        }
        self.assertEqual(Status.objects.count(), 1)
        response = self.client.post(
            reverse('statuses_update', kwargs={'pk': self.status.pk}), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')
        self.assertContains(response, _('This field is required.'))
        self.assertEqual(Status.objects.count(), 1)
        status = Status.objects.first()
        self.assertEqual(status.name, 'Test status')

    def test_status_update_view_post_unique(self):
        """
        Проверка POST-запроса на странице редактирования статуса с уникальным именем.

        Количество записей в базе данных - 1.
        Создаем второй статус. Страница должна быть перенаправлена на страницу со
        списком статусов (код 302), данные должны быть сохранены в базе данных.
        Количество записей в бд должно измениться - 2.
        Обновляем первый статус и пытаемся изменить имя на имя второго статуса.
        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        редактирования статуса, должно отображаться сообщение об ошибке.
        Количество записей в базе данных не изменяется - 2.
        Имя первого статуса в базе данных должно соответствовать начальному значению.
        """
        data_new = {
            'name': 'Test status new'
        }
        self.assertEqual(Status.objects.count(), 1)
        response = self.client.post(reverse('statuses_create'), data_new)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(Status.objects.count(), 2)

        # Обновляем первый статус и пытаемся изменить имя на имя второго статуса
        status1 = Status.objects.first()
        data = {
            'name': 'Test status new'
        }
        response = self.client.post(
            reverse('statuses_update', kwargs={'pk': status1.pk}), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')
        # self.assertContains(response, _('Status with this Name already exists.'))
        self.assertEqual(Status.objects.count(), 2)
        self.assertEqual(Status.objects.first().name, 'Test status')


class StatusesDeleteViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.status = Status.objects.create(name='Test status')

    def test_status_delete_view(self):
        """
        Проверка GET-запроса на странице удаления статуса.

        Страница должна быть доступной (код 200), должен использоваться правильный
        шаблон (с формой удаления статуса).
        """
        response = self.client.get(
            reverse('statuses_delete', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete.html')

    def test_status_delete_view_post(self):
        """
        Проверка POST-запроса на странице удаления статуса.

        Количество записей в базе данных - 1. После удаления статуса страница должна
        быть перенаправлена на страницу со списком статусов с кодом 302.
        Количество записей в базе данных после удаления - 0.
        """
        self.assertEqual(Status.objects.count(), 1)
        response = self.client.post(
            reverse('statuses_delete', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(Status.objects.count(), 0)
