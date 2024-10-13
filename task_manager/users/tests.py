from django.contrib.auth import get_user_model
from django.test import Client
from django.test.testcases import TestCase
from django.urls import reverse

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


class UserIndexViewTest(TestCase):
    def test_user_index_view_get(self):
        """
        Проверка GET-запроса на странице списка пользователей.

        Страница должна быть доступной (код 200), должен использоваться правильный
        шаблон (список пользователей).
        """
        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')


class UserCreateViewTest(TestCase):
    def test_user_create_view_get(self):
        """
        Проверка GET-запроса на странице создания пользователя.

        Страница должна быть доступной (код 200), должен использоваться правильный
        шаблон (с формой регистрации).
        """
        response = self.client.get(reverse('users_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')

    def test_user_create_view_post_valid(self):
        """
        Проверка POST-запроса на странице создания пользователя с валидными данными.

        Количество записей в базе данных - 0.
        Создаем нового пользователя.
        Страница должна быть перенаправлена на главную страницу (код 302), данные должны
        быть сохранены в базе данных (количество записей в бд должно увеличиться на 1).
        """
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123'
        }
        self.assertEqual(User.objects.count(), 0)
        response = self.client.post(reverse('users_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))
        self.assertEqual(User.objects.count(), 1)

    def test_user_create_view_post_invalid(self):
        """
        Проверка POST-запроса на странице создания пользователя с невалидными данными.

        Создаем нового пользователя (невалидные данные).
        Страница должна быть доступной (код 200), должен использоваться шаблон с формой
        регистрации, количество записей в базе данных не изменяется - 0.
        """
        data = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'password1': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(reverse('users_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')
        self.assertEqual(User.objects.count(), 0)


class UserUpdateViewTest(BaseTestCase):
    def test_user_update_view_get(self):
        """
        Проверка GET-запроса на странице редактирования пользователя.

        Страница должна быть доступной (код 200), должен использоваться правильный
        шаблон (с формой редактирования пользователя).
        """
        response = self.client.get(reverse('users_update', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')

    def test_user_update_view_post_valid(self):
        """
        Проверка POST-запроса на странице редактирования пользователя с валидными
        данными.

        Изменяем данные пользователя.
        Страница должна перенаправляться на страницу списка пользователей с кодом 302,
        после сохранения пользователь должен выйти из сессии, данные пользователя в базе
        данных должны измениться.
        """
        data = {
            'first_name': 'New Test',
            'last_name': 'New User',
            'username': 'newtestuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(
            reverse('users_update', args=[self.user.pk]),
            data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))
        self.assertFalse(self.client.session.get('user_id'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'New Test')
        self.assertEqual(self.user.last_name, 'New User')
        self.assertEqual(self.user.username, 'newtestuser')

    def test_user_update_view_post_invalid(self):
        """
        Проверка POST-запроса на странице редактирования пользователя с невалидными
        данными.

        Изменяем данные пользователя (невалидные данные).
        Страница должна быть доступной (код 200), должен использоваться правильный
        шаблон (с формой редактирования пользователя), данные пользователя в базе данных
        не должны измениться.
        """
        data = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(
            reverse('users_update', args=[self.user.pk]),
            data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.username, 'testuser')


class UserDeleteViewTest(BaseTestCase):
    def test_user_delete_view_get(self):
        """
        Проверка GET-запроса на странице удаления пользователя.

        Количество пользователей в базе данных должно быть равно единице.
        Страница должна быть доступной (код 200), должен использоваться правильный
        шаблон (с формой удаления пользователя).
        """
        self.assertEqual(User.objects.count(), 1)
        response = self.client.get(reverse('users_delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')

    def test_user_delete_view_post(self):
        """
        Проверка POST-запроса на странице удаления пользователя.

        Удаляем пользователя.
        Страница должна перенаправляться на страницу списка пользователей с кодом 302,
        количество пользователей в базе данных должно быть уменьшено на единицу,
        удаленная запись должна отсутствовать в базе данных.
        """
        response = self.client.post(reverse('users_delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))
        self.assertEqual(User.objects.count(), 0)
        self.assertQuerySetEqual(User.objects.filter(pk=self.user.pk), [])


class ChangeOtherUserProfileTest(TestCase):
    def setUp(self):
        """
        Создание двух пользователей для тестирования.
        """
        self.user1 = User.objects.create_user(
            first_name='Test1',
            last_name='User1',
            username='testuser1',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            first_name='Test2',
            last_name='User2',
            username='testuser2',
            password='password123'
        )

    def test_authorized_user_cannot_change_other_user_profile(self):
        """
        Проверяет, что авторизованный пользователь не может изменить или удалить профиль
        другого пользователя.

        Авторизуем пользователя user1.
        Количество пользователей в базе данных должно быть равно двум.
        Пытаемся изменить профиль пользователя user2.
        Страница должна перенаправляться на страницу списка пользователей с кодом 302.
        Пытаемся удалить профиль пользователя user2.
        Страница должна перенаправляться на страницу списка пользователей с кодом 302.
        Проверяем, что профиль пользователя user2 не был изменен или удален.
        Количество пользователей в базе данных должно быть равно двум (без изменений).
        """
        self.client.force_login(self.user1)
        self.assertEqual(User.objects.count(), 2)

        # пробуем изменить профиль пользователя user2
        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user2.pk}),
            data={'username': 'Buzz', 'first_name': 'Bar'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))

        # пробуем удалить профиль пользователя user2
        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.user2.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))

        self.user2.refresh_from_db()
        self.assertEqual(self.user2.username, 'testuser2')
        self.assertEqual(self.user2.first_name, 'Test2')
        self.assertEqual(User.objects.count(), 2)

    def test_not_authorized_user_cannot_change_other_user_profile(self):
        """
        Проверяет, что неавторизованный пользователь не может изменить или удалить
        профиль другого пользователя.

        Количество пользователей в базе данных должно быть равно двум.
        Пытаемся изменить профиль пользователя user1.
        Страница должна перенаправляться на страницу списка пользователей с кодом 302.
        Пытаемся удалить профиль пользователя user1.
        Страница должна перенаправляться на страницу списка пользователей с кодом 302.
        Проверяем, что профиль пользователя user1 не был изменен или удален.
        Количество пользователей в базе данных должно быть равно двум (без изменений).
        """
        self.assertEqual(User.objects.count(), 2)

        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user1.pk}),
            data={'username': 'Buzz', 'first_name': 'Bar'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.user1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'testuser1')
        self.assertEqual(self.user1.first_name, 'Test1')
        self.assertEqual(User.objects.count(), 2)


class UserLoginTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_user_login(self):
        """
        Проверяет, что пользователь может войти в систему

        Авторизуем пользователя user.
        Страница должна перенаправляться на страницу списка задач с кодом 302.
        """

        response = self.client.post(
            reverse('login'),
            data={'username': 'testuser', 'password': 'password123'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))


class UserLogoutTest(BaseTestCase):
    def test_user_logout(self):
        """
        Проверяет, что пользователь может выйти из системы

        Пытаемся выйти из системы.
        Страница должна перенаправляться на главную страницу с кодом 302.
        """
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
