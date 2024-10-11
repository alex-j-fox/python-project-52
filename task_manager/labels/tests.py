from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label

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
        Проверка доступности страницы со списком меток без авторизации.

        Страница должна быть доступна только авторизованным пользователям.
        Неавторизованный пользователь перенаправляется на страницу входа с кодом 302.
        """
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_unauthorized_create(self):
        """
        Проверка доступности страницы создания метки без авторизации.

        Страница должна быть доступна только авторизованным пользователям.
        Неавторизованный пользователь перенаправляется на страницу входа с кодом 302.
        """
        response = self.client.get(reverse('labels_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_unauthorized_update(self):
        """
        Проверка доступности страницы изменения метки без авторизации.

        Страница должна быть доступна только авторизованным пользователям.
        Неавторизованный пользователь перенаправляется на страницу входа с кодом 302.
        """
        response = self.client.get(reverse('labels_update', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_unauthorized_delete(self):
        """
        Проверка доступности страницы удаления метки без авторизации.

        Страница должна быть доступна только авторизованным пользователям.
        Неавторизованный пользователь перенаправляется на страницу входа с кодом 302
        """
        response = self.client.get(reverse('labels_delete', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class LabelsIndexViewTest(BaseTestCase):
    def test_labels_index_view(self):
        """
        Проверка GET-запроса на страницу со списком меток.

        Страница должна быть доступна (код 200) с использованием шаблона списка меток.
        """
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/index.html')


class LabelsCreateViewTest(BaseTestCase):
    def test_label_create_view_get(self):
        """
        Проверка GET-запроса на странице создания метки.

        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        создания метки.
        """
        response = self.client.get(reverse('labels_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/create.html')

    def test_label_create_view_post_valid(self):
        """
        Проверка POST-запроса на странице создания метки с валидными данными.

        Количество записей в базе данных - 0. После создания новой метки
        страница должна быть перенаправлена на страницу со списком меток (код 302),
        данные должны быть сохранены в базе данных.
        Количество записей в бд должно увеличиться на 1.
        Имя метки в базе данных должно соответствовать введенному значению.
        """
        data = {
            'name': 'Test label'
        }
        self.assertEqual(Label.objects.count(), 0)
        response = self.client.post(reverse('labels_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), 1)
        label = Label.objects.first()
        self.assertEqual(label.name, 'Test label')

    def test_label_create_view_post_invalid(self):
        """
        Проверка POST-запроса на странице создания метки с невалидными данными.

        Создаем новую метку (невалидные данные).
        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        создания метки, количество записей в базе данных не изменяется - 0.
        Должно быть отображено сообщение об ошибке.
        """
        data = {
            'name': ''
        }
        response = self.client.post(reverse('labels_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/create.html')
        self.assertContains(response, _('This field is required.'))
        self.assertEqual(Label.objects.count(), 0)

    def test_label_create_view_post_unique(self):
        """
        Проверка POST-запроса на странице создания метки с уникальным названием.

        Количество записей в базе данных - 0.
        Создаем новую метку. Страница должна быть перенаправлена на страницу со списком
        меток (код 302), данные должны быть сохранены в базе данных.
        Количество записей в бд должно увеличиться на 1.
        Создаем еще одну метку с тем же именем.
        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        создания метки, количество записей в базе данных не изменяется - 1.
        Должно быть отображено сообщение об ошибке.
        """
        data = {
            'name': 'Test label'
        }
        self.assertEqual(Label.objects.count(), 0)
        self.client.post(reverse('labels_create'), data)
        # Создаем еще один статус с тем же именем
        response = self.client.post(reverse('labels_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/create.html')
        self.assertContains(response, _('Label with this Name already exists.'))
        self.assertEqual(Label.objects.count(), 1)


class LabelsUpdateViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.label = Label.objects.create(name='Test label')

    def test_label_update_view_get(self):
        """
        Проверка GET-запроса на странице редактирования метки.

        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        редактирования метки.
        """
        response = self.client.get(
            reverse('labels_update', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/update.html')

    def test_label_update_view_post_valid(self):
        """
        Проверка POST-запроса на странице редактирования метки с валидными данными.

        Количество записей в базе данных - 1.
        Изменяем имя метки. Страница должна быть перенаправлена на страницу со списком
        меток (код 302), данные должны быть сохранены в базе данных.
        Количество записей в бд не должно измениться.
        Имя метки в базе данных должно соответствовать введенному значению.
        """
        data = {
            'name': 'Test label updated'
        }
        self.assertEqual(Label.objects.count(), 1)
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': self.label.pk}), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), 1)
        label = Label.objects.first()
        self.assertEqual(label.name, 'Test label updated')

    def test_label_update_view_post_invalid(self):
        """
        Проверка POST-запроса на странице редактирования метки с невалидными данными.

       Количество записей в базе данных - 1.
        Пытаемся изменить имя на пустую строку.
        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        редактирования метки, количество записей в базе данных не должно изменяться.
        Должно появляться сообщение об ошибке.
        Имя метки не должно измениться.
        """
        data = {
            'name': ''
        }
        self.assertEqual(Label.objects.count(), 1)
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': self.label.pk}), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/update.html')
        self.assertContains(response, _('This field is required.'))
        self.assertEqual(Label.objects.count(), 1)
        label = Label.objects.first()
        self.assertEqual(label.name, 'Test label')

    def test_label_update_view_post_unique(self):
        """
        Проверка POST-запроса на странице редактирования метки с уникальным именем.

        Количество записей в базе данных - 1.
        Создаем вторую метку. Страница должна быть перенаправлена на страницу со
        списком меток (код 302), данные должны быть сохранены в базе данных.
        Количество записей в бд должно измениться - 2.
        Обновляем первую метку и пытаемся изменить имя на имя второй метки.
        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        редактирования метки, должно отображаться сообщение об ошибке.
        Количество записей в базе данных не изменяется - 2.
        Имя первой метки в базе данных должно соответствовать начальному значению.
        """
        data_new = {
            'name': 'Test label new'
        }
        self.assertEqual(Label.objects.count(), 1)
        response = self.client.post(reverse('labels_create'), data_new)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), 2)

        # Обновляем первую метку и пытаемся изменить имя на имя вторй метки
        label1 = Label.objects.first()
        data = {
            'name': 'Test label new'
        }
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': label1.pk}), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/update.html')
        self.assertContains(response, _('Label with this Name already exists.'))
        self.assertEqual(Label.objects.count(), 2)
        self.assertEqual(Label.objects.first().name, 'Test label')


class LabelsDeleteViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.label = Label.objects.create(name='Test label')

    def test_label_delete_view(self):
        """
        Проверка GET-запроса на странице удаления метки.

        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        удаления метки.
        """
        response = self.client.get(
            reverse('labels_delete', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/delete.html')

    def test_label_delete_view_post(self):
        """
        Проверка POST-запроса на странице удаления метки.

        Количество записей в базе данных - 1. После удаления метки страница должна
        быть перенаправлена на страницу со списком меток с кодом 302.
        Количество записей в базе данных после удаления - 0.
        """
        self.assertEqual(Label.objects.count(), 1)
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), 0)
